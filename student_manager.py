import json
import os

# -------------------------
# Student Class
# -------------------------
class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        """Convert object to dictionary for JSON serialization"""
        return {
            "id": self.student_id,
            "name": self.name,
            "grade": self.grade
        }

# -------------------------
# StudentManager Class
# -------------------------
class StudentManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = self.load_students()

    def load_students(self):
        """Load data from JSON file"""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                return [Student(**s) for s in data]
        return []

    def save_students(self):
        """Save all student data to file"""
        with open(self.filename, "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    def add_student(self, student_id, name, grade):
        """Add a new student (unique ID validation)"""
        if any(s.student_id == student_id for s in self.students):
            print("❌ Student ID already exists!")
            return
        student = Student(student_id, name, grade)
        self.students.append(student)
        self.save_students()
        print("✅ Student added successfully!")

    def update_student(self, student_id, name=None, grade=None):
        """Update name or grade of a student"""
        for s in self.students:
            if s.student_id == student_id:
                if name:
                    s.name = name
                if grade:
                    s.grade = grade
                self.save_students()
                print("✅ Student updated successfully!")
                return
        print("❌ Student ID not found!")

    def delete_student(self, student_id):
        """Delete a student by ID"""
        for s in self.students:
            if s.student_id == student_id:
                self.students.remove(s)
                self.save_students()
                print("✅ Student deleted successfully!")
                return
        print("❌ Student ID not found!")

    def list_students(self):
        """Display all students in formatted table"""
        if not self.students:
            print("📂 No student records found.")
            return
        print("\n{:<10} {:<20} {:<10}".format("ID", "Name", "Grade"))
        print("-" * 40)
        for s in self.students:
            print("{:<10} {:<20} {:<10}".format(s.student_id, s.name, s.grade))
        print("-" * 40)

# -------------------------
# CLI Menu
# -------------------------
def main():
    manager = StudentManager()

    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. List Students")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            sid = input("Enter ID: ")
            name = input("Enter name: ")
            grade = input("Enter grade: ")
            manager.add_student(sid, name, grade)

        elif choice == "2":
            sid = input("Enter ID to update: ")
            name = input("Enter new name (leave blank to skip): ")
            grade = input("Enter new grade (leave blank to skip): ")
            manager.update_student(sid, name if name else None, grade if grade else None)

        elif choice == "3":
            sid = input("Enter ID to delete: ")
            manager.delete_student(sid)

        elif choice == "4":
            manager.list_students()

        elif choice == "5":
            print("👋 Exiting... Goodbye!")
            break

        else:
            print("❌ Invalid choice! Try again.")

if __name__ == "__main__":
    main()
