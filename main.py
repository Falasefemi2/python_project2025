from book_oop import BookManagementSystem

def main():
    """Main System"""
    book_system = BookManagementSystem()
    
    book_system.load_data()
    
    book_system.main_menu()

if __name__ == "__main__":
    main()