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
    
    def add_grade():
        # Add Student grade
        student_id = input("Enter student ID: ").strip()
        if not student_id:
            print("Error: Student ID cannot be empty")
            return
        if student_id not in students:
            print("Error: Student ID not found")
            return
        
        subject = input("Enter Subject name: ").strip()
        if not subject:
            print("Error: Subject name cannot be empty")
            return
        
        try:
            grade = float(input(f"Enter grade for {subject}: ").strip())
            if grade < 0 or grade > 100:
                print("Error: Grade should be between 0-100")
                return
        except ValueError:
            print("Invalid input. Please input a number")
            return
        students[student_id]["grades"][subject] = grade
        print(f"Grade for {subject} added successfully!")
    
    def add_multiple_grade():
        # Add Multiple grade
        student_id = input("Enter student ID: ").strip()
        if not student_id:
            print("Error: Student ID cannot be empty")
            return
        
        if student_id not in students:
            print("Error: Student ID not found")
            return
        
        print("Enter grades in this format 'subject:grade'. Type 'done' to finish.")
        while True:
            entry = input("Enter subject and grade: ").strip()
            if entry.lower() == "done":
                break
            
            try:
                subject, grade = entry.split(":")
                subject = subject.strip()
                grade = float(grade.strip())
                
                if grade < 0 or grade > 100:
                    print(f"Error: Grade for {subject} should be between 0-100")
                    continue
                
                students[student_id]["grades"][subject] = grade
                print(f"Grade for {subject} added successfully")
                
            except ValueError:
                print("Invalid input")        
    
    try:
        while True:
            print("\n===Welcome to Femi School===")
            print("1. Add Student")
            print("2. Save Data")
            print("3. Add Grade")
            print("4. Add Multiple grade")
            print("5. Exit")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                add_student()
            elif choice == "2":
                save_data()
            elif choice == "3":
                add_grade()
            elif choice == "4":
                add_multiple_grade()
            elif choice == "5":
                print("Exit Program")
                break
            else:
                print("Invalid Input")
    except Exception as e:
        print(f"Unexpected Error {e}")
     
if __name__ == "__main__":
    school_system()