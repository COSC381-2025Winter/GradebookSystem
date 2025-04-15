import datetime
import csv
import os
from data import COURSES, STUDENTS, ROSTERS
from color_ui import print_success, print_error, print_information, print_warning
from util import clear_screen

class Gradebook:
    def __init__(self, file_path="grades.csv"):
        self.csv_path = file_path
        self.grades = {}
        self.load_grades()


    def load_grades(self):
        if os.path.exists(self.csv_path):
            with open(self.csv_path, newline="") as f:

                reader = csv.DictReader(f)
                for row in reader:
                    course_id = row["course_id"]
                    student_id = int(row["student_id"])
                    grade = float(row["grade"])
                    timestamp = datetime.datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                    if course_id not in self.grades:
                        self.grades[course_id] = {}
                    self.grades[course_id][student_id] = {
                        "grade": grade,
                        "timestamp": timestamp
                    }

    def save_grades(self):
        with open(self.csv_path, "w", newline="") as f:
            fieldnames = ["course_id", "student_id", "grade", "timestamp"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for course_id, students in self.grades.items():
                for student_id, entry in students.items():
                    writer.writerow({
                        "course_id": course_id,
                        "student_id": student_id,
                        "grade": entry["grade"],
                        "timestamp": entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                    })

    def add_grade(self, instructor, course_id, student_id, grade):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to grade this course.")
            input("Press enter to continue.")
            return

        if course_id not in self.grades:
            self.grades[course_id] = {}

        now = datetime.datetime.now()

        if student_id in self.grades[course_id]:
            print_error("Error: Grade already exists. Use 'edit' instead.")
            input("Press enter to continue.")
        else:
            self.grades[course_id][student_id] = {"grade": grade, "timestamp": now}
            self.save_grades()
            print_success(f"Grade added for student {student_id}: {grade}")
            input("Press enter to continue.")

    def edit_grade(self, instructor, course_id, student_id, new_grade):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to edit this course.")
            input("Press enter to continue.")
            return

        if course_id in self.grades and student_id in self.grades[course_id]:
            old_timestamp = self.grades[course_id][student_id]["timestamp"]
            now = datetime.datetime.now()
            delta = now - old_timestamp

            if delta.days <= 7:
                self.grades[course_id][student_id] = {"grade": new_grade, "timestamp": now}
                self.save_grades()
                print_success(f"Grade updated for student {student_id}: {new_grade}")
                input("Press enter to continue.")
            else:
                print_error("Error: Grade editing period (7 days) has expired.")
                input("Press enter to continue.")
        else:
            print_error("Error: No existing grade found. Use 'add' instead.")
            input("Press enter to continue.")

    def view_grades(self, instructor, course_id):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to view this course.")
            input("Press enter to continue.")
            return

        if course_id in self.grades:
            print_information(f"\nGrades for {COURSES[course_id]['name']} ({course_id}):")
            for student_id, data in self.grades[course_id].items():
                student_name = STUDENTS[student_id]
                print_information(f"{student_name} ({student_id}): {data['grade']}")
        else:
            print_warning("No grades have been entered for this course yet.")
        
        input("Press enter to continue.")

    def sort_courses(self, arrangement_type):
        if not self.grades:
            print("Grades are empty. Please add a grade")
            input("Press enter to continue.")
            return

        if arrangement_type != 'a' and arrangement_type != 'd':
            print("Please type either (a/d)")
            input("Press enter to continue.")
            return

        if arrangement_type == 'd':
            sorted_grades = {course: dict(sorted(students.items(), key=lambda item: item[1]["grade"])) for course, students in self.grades.items()}
        elif arrangement_type == 'a':
            sorted_grades = {course: dict(sorted(students.items(), key=lambda item: item[1]["grade"], reverse=True)) for course, students in self.grades.items()}

        self.grades = sorted_grades

    def grades_to_edit(self, instructor, course_id):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to view this course.")
            input("Press enter to continue.")
            return

        if course_id in self.grades:
            print_information(f"\nGrades for {COURSES[course_id]['name']} ({course_id}):")
            for student_id, data in self.grades[course_id].items():
                student_name = STUDENTS[student_id]
                print_information(f"{student_name} ({student_id}): {data['grade']}")
            return True
        else:
            print_warning("No grades have been entered for this course yet. Use 'add' instead")
            input("Press enter to continue.")
            return False

    def search_student(self, course_id, query):
        matches = []
        query_str = str(query).lower()
        for student_id in ROSTERS[course_id]:
            student_name = STUDENTS.get(student_id, "Unknown")
            if query_str in student_name.lower() or query == str(student_id):
                matches.append((student_id, student_name))

        if matches:
            print("\nMatching Students:")
            for sid, name in matches:
                print(f"- {name} (ID: {sid})")
        else:
            print("No matching students found.")

    def helper_search_student(self, course_id):
        answer = True
        while (answer):
            answer = input("Would you like to search for students by ID/name?(y/n): ")
            if answer.lower() == "y":
                answer = False
                while True:
                    clear_screen()
                    print("========Search Student=========")
                    query = input("Enter Student ID or Name to search (or type 'back' to return): ")

                    if query.lower() == 'back':
                        break

                    self.search_student(course_id, query)
                    input("\nPress enter to continue searching or type 'back' in the next prompt.")

            elif answer.lower() == "n":
                answer = False
                break

            else:
                print("invalid input")
