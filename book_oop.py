import json
import random

class BookManagementSystem:
    """Book System"""
    def __init__(self):
        self.books = {}
        self.file_name = "store.json"
        
    def load_data(self):
        """Load data from file"""
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                book_data = json.load(file)
                self.books.update(book_data)
                print("Data loaded successfully.")
        except FileNotFoundError:
            print("No data file found. Starting with an empty library.")
        except json.JSONDecodeError:
            print("Error: File might be corrupted.")
        except Exception as e:
            print(f"Unexpected error while loading data: {e}")
    
    def save_data(self):
        """Save data to json file"""
        try:
            with open(self.file_name, "w", encoding="utf-8") as file:
                json.dump(self.books, file, indent=4)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Unexpected error while saving data: {e}")

    
    def generate_id(self):
        """Generate unique ID"""
        while True:
            book_id = str(random.randint(10000, 99999))
            if book_id not in self.books:
                return book_id
            
    def register_book(self):
        """Register book to file"""
        try:
            title = input("Enter book title: ").strip()
            author = input("Enter book author: ").strip()
            isbn = input("Enter book ISBN: ").strip()
            genre = input("Enter book genre: ").strip()
            copies = input("Enter number of copies: ").strip()
            
            if not copies.isdigit() or int(copies) <= 0:
                print("Error: Number of copies must be a positive integer.")
                return
            
            locations = ["Top Shelf", "Middle Shelf", "Bottom Shelf"]
            print("\nChoose Location for book")
            for idx, loc in enumerate(locations, start=1):
                print(f"{idx}. {loc}")
                
            location_choice = input("Choose the number corresponding to book location:").strip()
            
            if not location_choice.isdigit() or int(location_choice) not in range(1, len(locations) + 1):
                print("Error: Invalid input")
                return
            
            location = locations[int(location_choice) - 1]
            
            book_id = self.generate_id()
            self.books[book_id] = {
                "title": title,
                "author": author,
                "isbn": isbn,
                "genre": genre,
                "copies": copies,
                "location": location
            }
            
            print("\nBook Added successfully")
            print(f"Book with {book_id} added successfully")
        except Exception as e:
            print(f"Error while registering book: {e}")
    
    def edit_book(self):
        """Edit book"""
        book_id = input("Enter book ID: ").strip()
        if not book_id:
            print("Error: Book ID cannot be empty")
            return
        if book_id not in self.books:
            print("Error: Book ID not found")
            return
        
        book = self.books[book_id]
        print("\nCurrent Book Details")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"ISBN: {book['isbn']}")
        print(f"Genre: {book['genre']}")
        print(f"Copies: {book['copies']}")
        print(f"Location: {book['location']}")
        
        print("\nEdit new details: (Leave empty to retain details)")
        new_title = input(f"Title: [{book['title']}]: ").strip() or book['title']
        new_author = input(f"Author: [{book['author']}]: ").strip() or book['author']
        new_isbn = input(f"ISBN: [{book['isbn']}]: ").strip() or book['isbn']
        new_genre = input(f"Genre: [{book['genre']}]: ").strip() or book['genre'] 
        new_copies = input(f"Copies: [{book['copies']}]: ").strip()
        
        if new_copies.isdigit() and int(new_copies) > 0:
            new_copies = int(new_copies)   
        else:
            print("Invalid input for copies. Keeping the current value.")
            new_copies = book['copies']
        
        locations = ["Top Shelf", "Middle Shelf", "Bottom Shelf"]
        print("Choose a location (press Enter to keep the current value):")
        for idx, loc in enumerate(locations, 1):
            print(f"{idx}. {loc}")
        location_choice = input(f"Location [{book['location']}]: ").strip()
        if location_choice.isdigit() and 1 <= int(location_choice) <= len(locations):
            new_location = locations[int(location_choice) - 1]
        else:
            print("Invalid input for location. Keeping the current value.")
            new_location = book['location']
        
        self.books[book_id] = {
            "title": new_title,
            "author": new_author,
            "isbn": new_isbn,
            "genre": new_genre,
            "copies": new_copies,
            "location": new_location
        }
        print(f"Book details updated successfully for ID {book_id}.")
        
            
        