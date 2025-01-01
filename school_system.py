import random
import re
import json 

def school_system():
    """_summary_

    Returns:
        _type_: _description_
    """
    students = {}
    
    def load_data():
        # Load data fromJSON file
        try: 
            with open("student.json", "r", encoding="utf-8") as file:
                loaded_data = json.load(file)
                students.update(loaded_data)
                print("Data loaded successfully")
        except FileNotFoundError:
            print("Error: No data saved found")
        except json.JSONDecodeError:
            print("Error: Reading the save data. File might be corrupted")
        except Exception as e:
            print(f"Error: Unexpected error loading file: {e}")
            
    load_data()
    
    def save_data():
        # Save Data to Json
        try:
            with open("student.json", "w", encoding="utf-8") as file:
                json.dump(students, file, indent=4)
            print("Data saved successfully")
        except Exception as e:
            print(f"Unexpected Error saving file: {e}")
            
    
    def validate_name(name):
        # Validate Student name
        if not re.match(r"^[a-zA-Z ]+$", name):
            return False
        if len(name) < 2 or len(name) > 50:
            return False
        return True
    
    def generate_id():
        # Generate ID for student
        while True:
            student_id = str(random.randint(10000, 99999))
            if student_id not in students:
                return student_id
            
    def add_student():
        # Add student to system
        name = input("Enter Student Name: ").strip()
        
        if not name:
            print("Error: Student name cannot be empty")
            return
        
        if not validate_name(name):
            print("Error: Student name must be between 2-50 and alphabet")
            return
        
        if any(student["name"].lower() == name.lower() for student in students.values()):
            print(f"Student '{name}' already exists")
            return
        
        student_id = generate_id()
        students[student_id] = {
            "name": name,
            "grades": {}
        }
        
        print("\nStudent Added Successfully")
        print(f"Student Name: {name}")
        print(f"Student ID: {student_id}")
        
    
    try:
        while True:
            print("\n===Welcome to Femi School===")
            print("1. Add Student")
            print("2. Save Data")
            print("3. Exit")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                add_student()
            elif choice == "2":
                save_data()
            elif choice == "3":
                print("Exit Program")
                break
            else:
                print("Invalid Input")
    except Exception as e:
        print(f"Unexpected Error {e}")
        
21288
if __name__ == "__main__":
    school_system()