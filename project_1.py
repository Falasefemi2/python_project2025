import json
import csv
import random


class Patient:
    """Class Patient"""
    def __init__(self, patient_id, name, gender, age):
        self.patient_id = patient_id
        self.name = name
        self.gender = gender
        self.age = age
    
    def display_details(self):
        """Display patient details"""
        return (
            f"Patient ID: {self.patient_id}, Name: {self.name}, "
            f"Age: {self.age}, Gender: {self.gender}"
        )


class Doctor:
    """Class Doctor"""
    def __init__(self, doctor_id, name, specialization, available_days):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.available_days = available_days
        
    def display_details(self):
        """Display doctor details"""
        return (
            f"Doctor ID: {self.doctor_id}, Name: {self.name}, "
            f"Specialization: {self.specialization}, Available Days: {self.available_days}"
        )


class Appointment:
    """Class Appointment"""
    def __init__(self, appointment_id, patient_id, doctor_id, date, time):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time
        
    def display_details(self):
        """Display appointment details"""
        return (
            f"Appointment ID: {self.appointment_id}, Patient ID: {self.patient_id}, "
            f"Doctor ID: {self.doctor_id}, Date: {self.date}, Time: {self.time}"
        )


class Hospital:
    """Class Hospital"""
    def __init__(self):
        self.patients = []
        self.doctors = []
        self.appointments = []
        
    # Patient management method
    def add_patient(self, patient):
        """Add patient"""
        self.patients.append(patient)
        print(f"Patient {patient.name} added successfully")
    
    def search_patient(self, patient_id):
        """Search for patient"""
        for patient in self.patients:
            if patient.patient_id == patient_id:
                return patient
        return None
    
    def display_patient(self):
        """Display patient"""
        if not self.patients:
            print("No patient recorded")
        else:
            for patient in self.patients:
                print(patient.display_details())
    
    # Doctor management method
    def add_doctor(self, doctor):
        """Add doctors"""
        self.doctors.append(doctor)
        print(f"Doctor {doctor.name} added successfully")
    
    def search_doctor(self, doctor_id):
        """Search for doctor"""
        for doctor in self.doctors:
            if doctor.doctor_id == doctor_id:
                return doctor
        return None

    def display_doctor(self):
        """Display doctor"""
        if not self.doctors:
            print("No doctor recorded")
        else:
            for doctor in self.doctors:
                print(doctor.display_details())
                
    # Appointment management method
    def book_appointment(self, appointment):
        """Book appointment"""
        patient = self.search_patient(appointment.patient_id)
        doctor = self.search_doctor(appointment.doctor_id)
        
        if not patient:
            print(f"No patient found with ID {appointment.patient_id}")
            return
        
        if not doctor:
            print(f"No doctor found with ID {appointment.doctor_id}")
            return
        
        self.appointments.append(appointment)
        print(f"Appointment booked successfully: {appointment.display_details()}")
    
    def display_appointment(self):
        """Display appointment"""
        if not self.appointments:
            print("No appointment booked.")
        else:
            for appointment in self.appointments:
                print(appointment.display_details())
    
    def save_to_json(self, patient_file='patients.json', doctor_file='doctors.json', appointment_file='appointments.json'):
        """Save data to json"""
        
        # Save patients
        with open(patient_file, "w", encoding="utf-8") as file:
            json.dump([patient.__dict__ for patient in self.patients], file, indent=4)

        # Save doctors
        with open(doctor_file, "w", encoding="utf-8") as file:
            json.dump([doctor.__dict__ for doctor in self.doctors], file, indent=4)
        
        # Save appointments
        with open(appointment_file, "w", encoding="utf-8") as file:
            json.dump([appointment.__dict__ for appointment in self.appointments], file, indent=4)
        
        print("Data saved to JSON files successfully.")
    
    def load_from_json(self, patient_file='patients.json', doctor_file='doctors.json', appointment_file='appointments.json'):
        """Load data from json"""
        try:
            # Load patients
            with open(patient_file, "r", encoding="utf-8") as file:
                patients_data = json.load(file)
                self.patients = [Patient(**data) for data in patients_data]  
            
            # Load doctors
            with open(doctor_file, "r", encoding="utf-8") as file:
                doctors_data = json.load(file)
                self.doctors = [Doctor(**data) for data in doctors_data]   
            
            # Load appointments  
            with open(appointment_file, "r", encoding="utf-8") as file:
                appointments_data = json.load(file)
                self.appointments = [Appointment(**data) for data in appointments_data]
        
        except FileNotFoundError:
            print("File not found")


def main():
    """Main function"""
    hospital = Hospital()
    
    def generate_patient_id(hospital):
        """Generate a unique patient ID"""
        while True:
            patient_id = str(random.randint(1000, 9999))
            if not any(patient.patient_id == patient_id for patient in hospital.patients):
                return patient_id

    def generate_doctor_id(hospital):
        """Generate a unique doctor ID"""
        while True:
            doctor_id = str(random.randint(1000, 9999))
            if not any(doctor.doctor_id == doctor_id for doctor in hospital.doctors):
                return doctor_id

    def generate_appointment_id(hospital):
        """Generate a unique appointment ID"""
        while True:
            appointment_id = str(random.randint(1000, 9999))
            if not any(appointment.appointment_id == appointment_id for appointment in hospital.appointments):
                return appointment_id
            
    print("\nWelcome to the Hospital Management System")
    
    while True:
        print("\nMenu")
        print("1. Add Patient")
        print("2. Add Doctor")
        print("3. Book Appointment")
        print("4. View Patients")
        print("5. View Doctors")
        print("6. View Appointments")
        print("7. Save Data")
        print("8. Load Data")
        print("9. Exit")
        
        choice = input("Enter your choice (1-9): ").strip()
        
        if choice == "1":
            # Add patient
            patient_id = generate_patient_id(hospital)
            name = input("Enter patient name: ").strip()
            age = input("Enter Patient age: ").strip()
            gender = input("Enter patient gender: ").strip()
            patient = Patient(patient_id, name, gender, age)
            hospital.add_patient(patient)
        
        elif choice == "2":
            # Add Doctor
            doctor_id = generate_doctor_id(hospital)
            name = input("Enter Doctor name: ").strip()
            specialization = input("Enter Doctor specialization: ").strip()
            available_days = input("Enter doctor available days: ").strip()
            doctor = Doctor(doctor_id, name, specialization, available_days)
            hospital.add_doctor(doctor)
        
        elif choice == "3":
            # Book appointment
            patient_id = input("Enter Patient ID: ").strip()
            doctor_id = input("Enter Doctor ID: ").strip()
            date = input("Enter Appointment Date (YYYY-MM-DD): ")
            time = input("Enter Appointment Time (HH:MM): ")
            appointment_id = generate_appointment_id(hospital)
            appointment = Appointment(appointment_id, patient_id, doctor_id, date, time)
            hospital.book_appointment(appointment)
        
        elif choice == "4":
            # View Patients
            print("\nPatients")
            hospital.display_patient()
        
        elif choice == "5":
            print("\nDoctors")
            hospital.display_doctor()
            
        elif choice == "6":
            print("\nAppointments")
            hospital.display_appointment()
        
        elif choice == "7":
            hospital.save_to_json()
        
        elif choice == "8":
            hospital.load_from_json()
        
        elif choice == "9":
            # Exit
            print("Exiting system. Goodbye")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
