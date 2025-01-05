import random
import json
from datetime import datetime, timedelta
import os

class BookManagementSystem:
    """Book System"""
    def __init__(self):
        self.books = {}
        self.users = {}
        self.borrowing_records = {}
        self.current_user = None
        self.data_file = "library_data.json"
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
                print("Data loaded successfully")
            else:
                self.create_admin_account()
        except Exception as e:
            print(f"Error Loading data: {e}")
            self.create_admin_account()
    
    def save_data(self):
        """Save system data into file"""
        try:
            data = {
                "books": self.books,
                "users": self.users,
                "borrowing_records": self.borrowing_records
            }
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            print("Data saved successfully")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def create_admin_account(self):
        """Create default admin account"""
        admin_id = "ADMIN001"
        self.users[admin_id] = {
            "username": "admin",
            "password": "admin123",
            "role": "admin",
            "email": "admin@library.com",
            "status": "active"
        }
        print("Default admin account created")
        print("Username: admin")
        print("Password: admin123")
        self.save_data()
    
    def login(self):
        """User login system"""
        while True:
            print("\n=== Library Management System Login ===")
            username = input("Username (or 'exit' to quit): ").strip()
            if username.lower() == "exit":
                return False
            
            password = input("Password: ").strip()
            
            # Find user by username
            user_id = None
            for uid, user_data in self.users.items():
                if user_data["username"] == username and user_data["password"] == password:
                    user_id = uid
                    break
            
            if user_id:
                self.current_user = user_id
                print(f"\nWelcome, {self.users[user_id]['name']}!")
                return True
            else:
                print("Invalid username or password. Please try again.")
    
    def register_user(self):
        """Register a new user"""
        print("\n=== User Registration ===")
        username = input("Enter username: ").strip()
        
        # Check if username exits
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
        print("Registration Successful")
        print(f"Your User ID is : {user_id}")
        self.save_data()     
    
    def _is_admin(self):
        """Check if the current user is an admin"""
        if self.current_user and self.users[self.current_user]['role'] == "admin":
            return True
        return False
    
    def add_book(self):
        """Add a new book to the system"""   
        if not self._is_admin():
            print("Only administrators can add books")
            return
        
        print("\n=== AAdd New Book ===")
        try:
            title = input("Enter book title: ").strip()
            author = input("Enter author: ").strip()
            isbn = input("Enter ISBN: ").strip()
            genre = input("Enter genre: ").strip()
            copies = input("Enter number of copies: ").strip()
            
            locations = ["Top Shelf", "Middle Shelf", "Bottom Shelf"]
            print("\nAvailable Locations:")
            for idx, loc in enumerate(locations, 1):
                print(f"{idx}. {loc}")
            location_choice = int(input("Choose location (1-3): ").strip())
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
                "available_copies": copies,
                "location": location,
                "added_date": datetime.now().strftime('%Y-%m-%d')
            }
            
            print(f"\nBook added successfully!")
            print(f"Book ID: {book_id}")
            self.save_data()
        except ValueError:
            print("Invalid input. Please enter a valid number for copies.")
        except Exception as e:
            print(f"Error adding book: {e}")
    
    def search_book(self):
        """Search for book"""
        print("\n=== Search Books ===")
        print("1. Search by Title")
        print("2. Search by Author")
        print("3. Search by Genre")
        print("4. View all books")
        
        choice = input("Enter your choice: ").strip()
        
        search_results = []
        if choice == "4":
            search_results = list(self.books.items())
        else:
            search_term = input("Enter search term: ").strip().lower()
            
            for book_id, book in self.books.items():
                if (choice == "1" and search_term in book['title'].lower()) or \
                    (choice == "2" and search_term in book['author'].lower()) or \
                    (choice == "3" and search_term in book['genre'].lower()):
                        search_results.append((book_id, book))
        
        if search_results:
            print("\nSearch Results:")
            for book_id, book in search_results:
                print(f"\nBook ID: {book_id}")
                print(f"Title: {book['title']}")
                print(f"Author: {book['author']}")
                print(f"Genre: {book['genre']}")
                print(f"Available Copies: {book['available_copies']}")
                print(f"Location: {book['location']}")
                print("-" * 40)
        else:
            print("No books found")