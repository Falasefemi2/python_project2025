import json
import random
from datetime import datetime, timedelta
import os

class BookManagementSystem:
    """_summary_
    """
    def __init__(self):
        self.books = {}
        self.users = {}
        self.borrowing_records = {}
        self.current_user = None
        self.data_file = "student_data.json"
        self.load_data()
    
    def load_data(self):
        """Load system data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.books = data.get("books", {})
                    self.users = data.get("users", {})
                    self.borrowing_records = data.get("borrowing_records", {})
                print("DATA LOADED SUCCESSFULLY")        
        except Exception as e:
            print(f"Error Loading data: {e}")
            self.create_admin_account()
    
    def save_data(self):
        """Save system data to file"""
        try:
            data = {
                "books": self.books,
                "users": self.users,
                "borrowing_records": self.borrowing_records
            }
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            print("DATA SAVED SUCCESSFULLY")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def create_admin_account(self):
        """Create a default admin account"""
        admin_id = "ADMIN001"
        self.users[admin_id] = {
            "username": "admin",
            "password": "admin123",
            "role": "admin",
            "name": "System Admin",
            "email": "admin@library.com",
            "status": "active"
        }
        print("Default admin account created")
        print("Username: Admin")
        print("Password: admin123")
        self.save_data()
    
    def login(self):
        """User Login system"""
        while True:
            print("\n=== Library Management System Login ===")
            username = input("Username (or 'exit' to quit): ").strip()
            if username.lower() == "exit":
                return False
            
            password = input("Password: ").strip()
            
            # Find user by username 
            user_id = None
            for uid, user_data in self.users.items():
                if user_data['username'] == username and user_data['password'] == password:
                    user_id = uid
                    break
            
            if user_id:
                self.current_user = user_id
                print(f"\nWelcome, {self.users[user_id]['name']}")
                return True
            else:
                print("Invalid username or password. Please try again.")
    
    
    def register_user(self):
        """Register a new user"""
        print("\nUser Registration")
        username = input("Enter username: ").strip()
        
        for user in self.users.values():
            if user['username'] == username:
                print("Username already exits. Please choose another.")
                return
        password = input("Enter password: ").strip()
        name = input("Enter full name: ").strip()
        email = input("Enter email: ").strip()
        
        # Generate user ID
        user_id = f"USER{str(random.randint(1000, 9999))}"
        while user_id in self.users:
            user_id = f"USER{str(random.randint(1000, 9999))}"
        
        self.users[user_id] = {
            "username": username,
            "password": password,
            "role": "user",
            "name": name,
            "email": email,
            "status": "active",
            "join_date": datetime.now().strftime('%Y-%m-%d')
        }
        
        print("\nRegistration successfull")
        print(f"Your User ID: {user_id}")
        self.save_data()
        
    def _is_admin(self):
        """Check if the current user is an admin"""
        if self.current_user and self.users[self.current_user]['role'] == 'admin':
            return True
    
    def add_book(self):
        """Add a new book to system"""
        if not self._is_admin:
            print("Only administrators can add books")
            return
        
        print("\n=== Add New Book ===")
        try:
            title = input("Enter book title: ").strip()
            author = input("Enter author: ").strip()
            isbn = input("Enter ISBN: ").strip()
            genre = input("Enter genre: ").strip()
            copies = int(input("Enter number of copies: ").strip())
            
            locations = ["Top Shelf", "Middle Shelf", "Bottom Shelf"]
            print("\nAvailable locations:")
            for idx, loc in enumerate(locations, 1):
                print(f"{idx}. {loc}")
            location_choice = int(input("Choose a location (1-3): ").strip())
            location = locations[location_choice - 1]
            
            book_id = f"BOOK{str(random.randint(1000, 9999))}"
            while book_id in self.books:
                book_id = f"BOOK{str(random.randint(1000, 9999))}"
                
            self.books[book_id] = {
                "title": title,
                "author": author,
                "isbn": isbn,
                "genre": genre,
                "copies": copies,
                "location": location,
                "added_data": datetime.now().strftime('%Y-%m-%d')
            }
            
            print("\nBook Added Successfully")
            print(f"Book ID: {book_id}")
            self.save_data()
        except ValueError:
            print("Invalid Input. Please enter a valid number for copies")
        except Exception as e:
            print(f"Error adding book: {e}")
    
    def search_book(self):
        """Search fot books"""
        print("\n=== Search Books ===")
        print("1. Search by Title")
        print("2. Search by Author")
        print("3. Search by Genre")
        print("4. View All Books")
        
        choice = input("Enter your choice: ").strip()
        
        search_result = []
        if choice == "4":
            search_result = list(self.books.items())
        else:
            search_term = input("Enter search term: ").strip().lower()
            
            for book_id, book in self.books.items():
                if (choice == "1" and search_term in book["title"].lower()) or \
                    (choice == "2" and search_term in book['author'].lower()) or \
                    (choice == "3" and search_term in book['genre'].lower()):
                        search_result.append((book_id, book))
            if search_result:
                print("\nSearch Result")
                for book_id, book in search_result:
                    print(f"\nBook ID: {book_id}")
                    print(f"Title: {book['title']}")
                    print(f"Author: {book['author']}")
                    print(f"Genre: {book['genre']}")
                    print(f"Copies: {book['copies']}")
                    print(f"Location: {book['location']}")
                    print("-" * 40)
            else:
                print("No books found")
    
    def borrow_book(self):
        """Borrow a book"""
        if not self.current_user:
            print("Please log in first.")
            return
        
        print("\n=== Borrow Book ===")
        book_id = input("Enter Book ID: ").strip()
        
        if book_id not in self.books:
            print("Book not found.")
            return
        
        book = self.books[book_id]
        if book['copies'] <= 0:
            print("No copies available for borrowing.")
            return
        
        # Prevent multiple borrowing of the same book
        if self.current_user in self.borrowing_records and book_id in self.borrowing_records[self.current_user]:
            print("You have already borrowed this book. Please return it before borrowing again.")
            return
        
        # Process the loan
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=14)
        
        if self.current_user not in self.borrowing_records:
            self.borrowing_records[self.current_user] = {}
        
        self.borrowing_records[self.current_user][book_id] = {
            "borrow_date": borrow_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "status": "borrowed"
        }
        
        book['copies'] -= 1
        
        print(f"\nBook '{book['title']}' borrowed successfully!")
        print(f"Due Date: {due_date.strftime('%Y-%m-%d')}")
        self.save_data()
    
    def return_book(self):
        """Return a borrowed book"""
        if not self.current_user:
            print("Please log in first.")
            return
        
        if self.current_user not in self.borrowing_records or not self.borrowing_records[self.current_user]:
            print("You have no books to return.")
            return
        
        print("\n=== Return Book ===")
        print("\nYour borrowed books:")
        for book_id, borrow_info in self.borrowing_records[self.current_user].items():
            book = self.books[book_id]
            print(f"\nBook ID: {book_id}")
            print(f"Title: {book['title']}")
            print(f"Due Date: {borrow_info['due_date']}")
        
        book_id = input("\nEnter Book ID to return: ").strip()
        
        if book_id not in self.borrowing_records[self.current_user]:
            print("Invalid Book ID or you haven't borrowed this book.")
            return
        
        # Process return
        book = self.books[book_id]
        borrow_info = self.borrowing_records[self.current_user][book_id]
        
        due_date = datetime.strptime(borrow_info['due_date'], "%Y-%m-%d").date()
        return_date = datetime.now().date()
        
        # Calculate late fees
        if return_date > due_date:
            days_late = (return_date - due_date).days
            late_fee = days_late * 1.00  # $1 per day
            print(f"\nLate Fee: ${late_fee:.2f}")
        
        book["copies"] += 1
        del self.borrowing_records[self.current_user][book_id]
        
        # Check if the user has returned all books
        if not self.borrowing_records[self.current_user]:
            del self.borrowing_records[self.current_user]
        
        print(f"\nBook '{book['title']}' returned successfully!")
        self.save_data()
        
    def view_borrowed_book(self):
        """View currently borrowed books"""
        if not self.current_user:
            print("Please log in first.")
            return
        
        print(f"\n=== Your Borrowed Books ===")
        if self.current_user not in self.borrowing_records or \
        not self.borrowing_records[self.current_user]:
            print("You haven't borrowed any books.")
            return
        
        for book_id, borrow_info in self.borrowing_records[self.current_user].items():
            book = self.books.get(book_id)  # Handle invalid records
            if not book:
                print(f"\nBook ID: {book_id} (Book data missing)")
                continue
            
            print(f"\nBook ID: {book_id}")
            print(f"Title: {book['title']}")
            print(f"Author: {book['author']}")
            print(f"Borrow Date: {borrow_info['borrow_date']}")
            print(f"Due Date: {borrow_info['due_date']}")
            
            # Calculate days remaining or overdue
            due_date = datetime.strptime(borrow_info['due_date'], '%Y-%m-%d').date()
            today = datetime.now().date()
            days_remaining = (due_date - today).days
            
            if days_remaining > 0:
                print(f"Days Remaining: {days_remaining} (On Time)")
            else:
                print(f"Overdue by: {abs(days_remaining)} days")
            print("-" * 40)
            
    def generate_reports(self):
        """Generate system reports"""
        if not self._is_admin():
            print("Only administrators can generate reports")
            return
        
        print(f"\n=== Generate Reports ===")
        print("1. Overdue Books Report")
        print("2. Books Status Report")
        print("3. User Activity Report")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            self._generate_overdue_report()
        elif choice == "2":
            self._generate_books_status_report()
        elif choice == "3":
            self._generate_user_activity_report()
        else:
            print("Invalid choice")
    
    def run(self):
        """Run the main program loop"""
        while True:
            print("\n=== Library Management System ===")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                if self.login():
                    self.main_menu()
            elif choice == "2":
                self.register_user()
            elif choice == "3":
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                
    def main_menu(self):
        """Display the main menu after login"""
        while True:
            print("\n=== Main Menu ===")
            print("1. Add Book")
            print("2. Search Books")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. View Borrowed Books")
            print("6. Generate Reports")
            print("7. Logout")
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.search_book()
            elif choice == "3":
                self.borrow_book()
            elif choice == "4":
                self.return_book()
            elif choice == "5":
                self.view_borrowed_book()
            elif choice == "6":
                self.generate_reports()
            elif choice == "7":
                self.current_user = None
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _is_admin(self):
        """Check if the current user is an admin"""
        if self.current_user and self.users[self.current_user]['role'] == 'admin':
            return True
        return False

    def _generate_overdue_report(self):
        """Generate report of overdue books"""
        print("\n=== Overdue Books Report ===")
        current_date = datetime.now().date()
        overdue_found = False

        for user_id, books in self.borrowing_records.items():
            user = self.users[user_id]
            for book_id, borrow_info in books.items():
                due_date = datetime.strptime(borrow_info['due_date'], '%Y-%m-%d').date()
                if current_date > due_date:
                    if not overdue_found:
                        overdue_found = True
                    book = self.books[book_id]
                    days_overdue = (current_date - due_date).days
                    print(f"\nBook: {book['title']}")
                    print(f"Borrowed by: {user['name']} (ID: {user_id})")
                    print(f"Due Date: {borrow_info['due_date']}")
                    print(f"Days Overdue: {days_overdue}")
                    print(f"Late Fee: ${days_overdue * 1.00:.2f}")

        if not overdue_found:
            print("No overdue books found.")

    def _generate_books_status_report(self):
        """Generate report of all books status"""
        print("\n=== Books Status Report ===")
        total_books = 0
        total_copies = 0
        borrowed_copies = 0

        for book_id, book in self.books.items():
            total_books += 1
            total_copies += book['copies']
            borrowed_copies += (book['copies'] - book['available_copies'])
            
            print(f"\nBook ID: {book_id}")
            print(f"Title: {book['title']}")
            print(f"Total Copies: {book['copies']}")
            print(f"Available Copies: {book['available_copies']}")
            print(f"Borrowed Copies: {book['copies'] - book['available_copies']}")
            print("-" * 40)

        print(f"\nSummary:")
        print(f"Total Books: {total_books}")
        print(f"Total Copies: {total_copies}")
        print(f"Borrowed Copies: {borrowed_copies}")
        print(f"Available Copies: {total_copies - borrowed_copies}")

    def _generate_user_activity_report(self):
        """Generate report of user activity"""
        print("\n=== User Activity Report ===")
        
        for user_id, user in self.users.items():
            if user['role'] == 'user':
                print(f"\nUser: {user['name']} (ID: {user_id})")
                print(f"Join Date: {user['join_date']}")
                

if __name__ == "__main__":
    library_system = BookManagementSystem()
    
    library_system.run()
    
    


                
                


