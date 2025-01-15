class User:
    def __init__(self, username, password, contact_info):
        """
        Initialize a user with a username, password, and contact information.
        Passwords should ideally be hashed for security.
        """
        self.username = username
        self.password = password  # In a real system, store hashed passwords
        self.contact_info = contact_info

    def update_contact_info(self, new_contact_info):
        """Update the user's contact information."""
        self.contact_info = new_contact_info

    def view_profile(self):
        """Return the user's profile details."""
        return {
            "Username": self.username,
            "Contact Info": self.contact_info
        }

    def authenticate(self, password):
        """
        Check if the provided password matches the user's password.
        This would typically involve hashing and comparing in a real system.
        """
        return self.password == password
    

class Doctor(User):
    def __init__(self, username, password, contact_info, name, specialty):
        """
        Initialize a doctor with additional attributes for their name and specialty.
        Inherits common attributes from the User class.
        """
        super().__init__(username, password, contact_info)
        self.name = name
        self.specialty = specialty
        self.availability = {}  # Dictionary to track available time slots (e.g., {"2025-01-15": ["10:00", "11:00"]})

    def add_availability(self, date, time_slots):
        """
        Add available time slots for a specific date.
        :param date: A string representing the date (e.g., "2025-01-15").
        :param time_slots: A list of time slots (e.g., ["10:00", "11:00"]).
        """
        if date in self.availability:
            self.availability[date].extend(time_slots)
        else:
            self.availability[date] = time_slots

    def update_availability(self, date, new_time_slots):
        """
        Update the availability for a specific date.
        Replaces the existing time slots for the given date.
        """
        self.availability[date] = new_time_slots

    def view_schedule(self):
        """Return the doctor's schedule, including all available time slots."""
        return {
            "Name": self.name,
            "Specialty": self.specialty,
            "Availability": self.availability
        }

class Patient(User):
    """
    Represents a patient, inheriting common attributes from the User class.
    Adds attributes for medical history and patient-specific methods.
    """
    def __init__(self, username, password, contact_info, name=None, age=None):
        super().__init__(username, password, contact_info)
        self.name = name
        self.age = age
        self.medical_history = []

    def add_medical_history(self, entry):
        """Add a new entry to the patient's medical history."""
        self.medical_history.append(entry)

    def view_details(self):
        """Return the patient's details, including medical history."""
        return {
            "Name": self.name,
            "Age": self.age,
            "Username": self.username,
            "Contact Info": self.contact_info,
            "Medical History": self.medical_history
        }

    def to_dict(self):
        """Return a dictionary representation of the patient."""
        return {
            "username": self.username,
            "password": self.password,  # Store only if hashed
            "contact_info": self.contact_info,
            "name": self.name,
            "age": self.age,
            "medical_history": self.medical_history
        }

    @staticmethod
    def from_dict(data):
        """Create a Patient object from a dictionary."""
        patient = Patient(
            username=data["username"],
            password=data["password"],  # Ensure secure handling of passwords
            contact_info=data["contact_info"],
            name=data.get("name"),
            age=data.get("age")
        )
        patient.medical_history = data.get("medical_history", [])
        return patient
    

class Appointment:
    """
    Represents an appointment between a doctor and a patient.
    """
    def __init__(self, appointment_id, doctor_id, patient_id, date, time, reason):
        """
        Initialize an appointment with doctor and patient references, date, time, and reason.
        """
        self.appointment_id = appointment_id
        self.doctor_id = doctor_id  # Reference to the doctor's ID or object
        self.patient_id = patient_id  # Reference to the patient's ID or object
        self.date = date
        self.time = time
        self.reason = reason
        self.status = "Scheduled"  # Possible values: Scheduled, Rescheduled, Canceled

    def reschedule(self, new_date, new_time):
        """
        Reschedule the appointment to a new date and time.
        """
        self.date = new_date
        self.time = new_time
        self.status = "Rescheduled"

    def cancel(self):
        """
        Cancel the appointment.
        """
        self.status = "Canceled"

    def view_details(self):
        """
        Return the details of the appointment.
        """
        return {
            "Appointment ID": self.appointment_id,
            "Doctor ID": self.doctor_id,
            "Patient ID": self.patient_id,
            "Date": self.date,
            "Time": self.time,
            "Reason": self.reason,
            "Status": self.status
        }

    def to_dict(self):
        """
        Return a dictionary representation of the appointment.
        """
        return {
            "appointment_id": self.appointment_id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "date": self.date,
            "time": self.time,
            "reason": self.reason,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """
        Create an Appointment object from a dictionary.
        """
        return Appointment(
            appointment_id=data["appointment_id"],
            doctor_id=data["doctor_id"],
            patient_id=data["patient_id"],
            date=data["date"],
            time=data["time"],
            reason=data["reason"]
        )

class Prescription:
    """
    Represents a prescription issued by a doctor for a patient.
    """
    def __init__(self, prescription_id, doctor_id, patient_id, date, medications):
        """
        Initialize a prescription with a unique ID, doctor and patient references, date, and medications.
        :param prescription_id: Unique identifier for the prescription.
        :param doctor_id: Reference to the doctor's ID or object.
        :param patient_id: Reference to the patient's ID or object.
        :param date: Date when the prescription was issued.
        :param medications: List of medications with dosage and instructions.
               Example: [{"name": "Paracetamol", "dosage": "500mg", "instructions": "Take one tablet every 8 hours"}]
        """
        self.prescription_id = prescription_id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.date = date
        self.medications = medications  # List of medication dictionaries

    def add_medication(self, name, dosage, instructions):
        """
        Add a medication to the prescription.
        :param name: Name of the medication.
        :param dosage: Dosage of the medication (e.g., "500mg").
        :param instructions: Usage instructions (e.g., "Take one tablet every 8 hours").
        """
        self.medications.append({
            "name": name,
            "dosage": dosage,
            "instructions": instructions
        })

    def view_details(self):
        """
        Return the details of the prescription.
        """
        return {
            "Prescription ID": self.prescription_id,
            "Doctor ID": self.doctor_id,
            "Patient ID": self.patient_id,
            "Date": self.date,
            "Medications": self.medications
        }

    def to_dict(self):
        """
        Return a dictionary representation of the prescription.
        """
        return {
            "prescription_id": self.prescription_id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "date": self.date,
            "medications": self.medications
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Prescription object from a dictionary.
        """
        return Prescription(
            prescription_id=data["prescription_id"],
            doctor_id=data["doctor_id"],
            patient_id=data["patient_id"],
            date=data["date"],
            medications=data["medications"]
        )


# Import your classes here, e.g., Patient, Doctor, Appointment, Prescription

# Sample storage for demonstration (in a real application, use file/database storage)
patients = {}
doctors = {}
appointments = {}
prescriptions = {}

def create_patient():
    """Create a new patient."""
    username = input("Enter username: ")
    password = input("Enter password: ")
    contact_info = input("Enter contact information: ")
    name = input("Enter name: ")
    age = input("Enter age: ")
    
    patient = Patient(username, password, contact_info, name, age)
    patients[username] = patient
    print("Patient created successfully!")

def create_doctor():
    """Create a new doctor."""
    username = input("Enter username: ")
    password = input("Enter password: ")
    contact_info = input("Enter contact information: ")
    name = input("Enter name: ")
    specialty = input("Enter specialty: ")
    
    doctor = Doctor(username, password, contact_info, name, specialty)
    doctors[username] = doctor
    print("Doctor created successfully!")

def schedule_appointment():
    """Schedule a new appointment."""
    appointment_id = input("Enter appointment ID: ")
    doctor_id = input("Enter doctor ID: ")
    patient_id = input("Enter patient ID: ")
    date = input("Enter appointment date (YYYY-MM-DD): ")
    time = input("Enter appointment time (HH:MM): ")
    reason = input("Enter reason for appointment: ")
    
    if doctor_id not in doctors or patient_id not in patients:
        print("Invalid doctor or patient ID!")
        return
    
    appointment = Appointment(appointment_id, doctor_id, patient_id, date, time, reason)
    appointments[appointment_id] = appointment
    print("Appointment scheduled successfully!")

def issue_prescription():
    """Issue a new prescription."""
    prescription_id = input("Enter prescription ID: ")
    doctor_id = input("Enter doctor ID: ")
    patient_id = input("Enter patient ID: ")
    date = input("Enter prescription date (YYYY-MM-DD): ")
    
    if doctor_id not in doctors or patient_id not in patients:
        print("Invalid doctor or patient ID!")
        return
    
    medications = []
    while True:
        name = input("Enter medication name (or 'done' to finish): ")
        if name.lower() == "done":
            break
        dosage = input("Enter dosage: ")
        instructions = input("Enter instructions: ")
        medications.append({"name": name, "dosage": dosage, "instructions": instructions})
    
    prescription = Prescription(prescription_id, doctor_id, patient_id, date, medications)
    prescriptions[prescription_id] = prescription
    print("Prescription issued successfully!")

def view_data():
    """View all data."""
    print("\n--- Patients ---")
    for patient in patients.values():
        print(patient.view_details())
    
    print("\n--- Doctors ---")
    for doctor in doctors.values():
        print(doctor.view_details())
    
    print("\n--- Appointments ---")
    for appointment in appointments.values():
        print(appointment.view_details())
    
    print("\n--- Prescriptions ---")
    for prescription in prescriptions.values():
        print(prescription.view_details())

def main():
    """Main function to run the CLI."""
    while True:
        print("\n--- Hospital Patient Records System ---")
        print("1. Create Patient")
        print("2. Create Doctor")
        print("3. Schedule Appointment")
        print("4. Issue Prescription")
        print("5. View All Data")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_patient()
        elif choice == "2":
            create_doctor()
        elif choice == "3":
            schedule_appointment()
        elif choice == "4":
            issue_prescription()
        elif choice == "5":
            view_data()
        elif choice == "6":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
