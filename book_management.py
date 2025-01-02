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

    def main_menu():
        """Display the main menu"""
        while True:
            print("\nBook Management System")
            print("1. Add Book")
            print("2. Save Data")
            print("3. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                register_book()
            elif choice == "2":
                save_data()
            elif choice == "3":
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
