import random
import json

def book_system():
    """Book Management System"""
    books = {}

    def load_data():
        """Load book data from a file"""
        try:
            with open("books.json", "r", encoding="utf-8") as file:
                book_data = json.load(file)
                books.update(book_data)
                print("Data loaded successfully.")
        except FileNotFoundError:
            print("No data file found. Starting with an empty library.")
        except json.JSONDecodeError:
            print("Error: File might be corrupted.")
        except Exception as e:
            print(f"Unexpected error while loading data: {e}")

    def save_data():
        """Save book data to a file"""
        try:
            with open("books.json", "w", encoding="utf-8") as file:
                json.dump(books, file, indent=4)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Unexpected error while saving data: {e}")

    def generate_book_id():
        """Generate a unique book ID"""
        while True:
            book_id = str(random.randint(10000, 99999))
            if book_id not in books:
                return book_id

    def register_book():
        """Register a new book"""
        try:
            title = input("Enter book title: ").strip()
            author = input("Enter book author: ").strip()
            isbn = input("Enter book ISBN: ").strip()
            genre = input("Enter book genre: ").strip()
            copies = input("Enter number of copies: ").strip()


            # Validate copies input
            if not copies.isdigit() or int(copies) <= 0:
                print("Error: Number of copies must be a positive integer.")
                return
            
            locations = ["Top Shelf", "Middle Shelf", "Bottom Shelf"]
            print("\nChoose a location for the book:")
            for idx, loc in enumerate(locations, start=1):
                print(f"{idx}. {loc}")
            
            location_choice = input("Enter the number corresponding to the location: ").strip()
            
            if not location_choice.isdigit() or int(location_choice) not in range(1, len(locations) + 1):
                print("Invalid choice. Location not updated.")
                return
            
            location = locations[int(location_choice) - 1]


            book_id = generate_book_id()
            books[book_id] = {
                "title": title,
                "author": author,
                "isbn": isbn,
                "genre": genre,
                "copies": int(copies),
                "location": location,
            }
            print(f"Book '{title}' added successfully with ID {book_id}.")
        except Exception as e:
            print(f"Error while registering book: {e}")
            
    def edit_book():
        # Edit book details
        book_id = input("Enter book ID: ").strip()
        if not book_id:
            print("Error: Book ID cannot be empty.")
            return
        
        if book_id not in books:
            print("Error: Book ID not found.")
            return
        
        book = books[book_id]
        print("\nCurrent Book details: ")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"ISBN: {book['isbn']}")
        print(f"Genre: {book['genre']}")
        print(f"Copies: {book['copies']}")
        print(f"Location: {book['location']}")
        
        print("\nEnter new details (leave empty to retain current value): ")
        new_title = input(f"Title: [{book['title']}]: ").strip() or book['title']
        new_author = input(f"Author: [{book['author']}]: ").strip() or book['author']
        new_isbn = input(f"ISBN: [{book['isbn']}]: ").strip() or book['isbn']
        new_genre = input(f"Genre: [{book['genre']}]: ").strip() or book['genre']
        
        # Validate copies input
        new_copies = input(f"Copies: [{book['copies']}]: ").strip() 
        if new_copies.isdigit() and int(new_copies) < 0:
            new_copies = int(new_copies)
        else:
            print("Invalid input for copies. Keeping the current value.")
            new_copies = book['copies']
        
        # Predefined locations
        locations = ["Top Shelf", "Middle Shelf", "Bottom Shelf"]
        print("Choose a location (press Enter to keep the current value):")
        for idx, loc in enumerate(locations, 1):
            print(f"{idx}. {loc}")
        location_choice = input(f"Location [{book['location']}]: ").strip()
        if location_choice.isdigit() and int(location_choice) in range(1, len(locations) + 1):
            new_location = locations[int(location_choice) - 1]
        else:
            print("Invalid input for location. Keeping the current value.")
            new_location = book['location']
            
            books[book_id] = {
                "title": new_title,
                "author": new_author,
                "isbn": new_isbn,
                "genre": new_genre,
                "copies": new_copies,
                "location": new_location,
            }
            
            print(f"Book details updated successfully for ID {book_id}.")
        
    def delete_book():
        # Delete book from system
        book_id = input("Enter book ID: ").strip()
        if book_id not in books:
            print("Error: Book ID not found.")
            return
        
        del books[book_id]
        print(f"Book with ID: {book_id} deleted successfully.")
    
    def search_book():
        # Search for a book by title or author
        print("\nSearch book by Title or Author: ")
        entry = input("Enter book title or author: ").strip().lower()

        if not entry:
            print("Error: Search term cannot be empty.")
            return

        matches = []
        for idx, book in enumerate(books.values(), start=1):
            if entry in book['title'].lower() or entry in book['author'].lower():
                matches.append((idx, book))

        if not matches:
            print("No books found matching the search term.")
            return

        print("\nMatching Books:")
        for idx, book in matches:
            print(f"{idx}. {book['title']} by {book['author']}")

        # Ask the user to select a book or go back to the main menu
        try:
            choice = int(input("\nEnter the number of the book to view details or 0 to return to main menu: "))
            if choice == 0:
                print("Returning to the main menu.")
                return

            # Display the selected book's details
            selected_book = matches[choice - 1][1]
            print("\nBook Details:")
            print(f"Title: {selected_book['title']}")
            print(f"Author: {selected_book['author']}")
            print(f"ISBN: {selected_book['isbn']}")
            print(f"Genre: {selected_book['genre']}")
            print(f"Copies Available: {selected_book['copies']}")
            print(f"Location: {selected_book['location']}")

        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except IndexError:
            print("Invalid book selection. Please try again.")
            
    def borrow_book():
        # Borrow a book
        book_id = input("Enter book ID: ").strip()
        
        if book_id not in books:
            print("Error: Book ID not found.")
            return
        
        book = books[book_id]
        
        if book['copies'] > 0:
            # Borrow book and reduce it by 1
            book['copies'] -= 1
            print(f"Book borrowed successfully: {book['title']} by {book['author']}")
            print(f"Remaining copies: {book['copies'] - 1}")
        
            # Save the updated data (if necessary)
            save_data()  # Ensure you save after borrowing
        else:
            print("Error: No copies available for borrowing.")


                            


        

    def main_menu():
        """Display the main menu"""
        while True:
            print("\nBook Management System")
            print("1. Add Book")
            print("2. Edit Book")
            print("3. Save Data")
            print("4. Delete Book")
            print("5. Search Book")
            print("6. Borrow Book")
            print("7. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                register_book()
            elif choice == "2":
                edit_book()
            elif choice == "3":
                save_data()
            elif choice == "4":
                delete_book()
            elif choice == "5":
                search_book()
            elif choice == "6":
                borrow_book()
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    # Load data and run the system
    load_data()
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting the system. Goodbye!")
        save_data()

if __name__ == "__main__":
    book_system()
