import datetime
from data import COURSES, STUDENTS, ROSTERS
from color_ui import print_success, print_error, print_information, print_warning
from util import clear_screen

class Gradebook:
    def __init__(self):
        self.grades = {}  # {course_id: {student_id: {"grade": x, "timestamp": y}}}

    def add_grade(self, instructor, course_id, student_id, grade):
        """Adds a grade for a student in a specific course"""
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to grade this course.")
            input("Press enter to continue.")
            return

        # Validate grade
        try:
            grade = int(grade)
            if not (0 <= grade <= 100):
                raise ValueError
        except ValueError:
            print_error("Grade must be an integer between 0 and 100.")
            input("Press enter to continue.")
            return

        if course_id not in self.grades:
            self.grades[course_id] = {}

        now = datetime.datetime.now()

        if student_id in self.grades[course_id]:
            option = input("Grade already exists. Do you want to edit it? (Y/N): ")
            if option.upper() == "Y":
                self.grades[course_id][student_id] = {
                    "grade": grade,
                    "timestamp": now
                }
                print_success(f"Grade updated for student {student_id}: {grade}")
            else:
                print_information("Grade not updated.")
        else:
            self.grades[course_id][student_id] = {"grade": grade, "timestamp": now}
            print_success(f"Grade added for student {student_id}: {grade}")
            print_success("\nGrade added successfully!")
            print_information("Press enter to continue.")
            input()

    def edit_grade(self, instructor, course_id, student_id, new_grade):
        """Edits an existing grade but only within 7 days of the first entry"""
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to edit this course.")
            input("Press enter to continue.")
            return

        # Validate new grade
        try:
            new_grade = int(new_grade)
            if not (0 <= new_grade <= 100):
                raise ValueError
        except ValueError:
            print_error("Grade must be an integer between 0 and 100.")
            input("Press enter to continue.")
            return

        if course_id in self.grades and student_id in self.grades[course_id]:
            old_data = self.grades[course_id][student_id]
            old_grade = old_data["grade"]
            old_timestamp = old_data["timestamp"]
            now = datetime.datetime.now()
            delta = now - old_timestamp

            if delta.days <= 7:
                print_warning(f"Current Grade for Student {student_id}: {old_grade}")
                confirmation = input(f"Are you sure you want to change it to {new_grade}? (y/n): ").strip().lower()
                if confirmation == 'y':
                    self.grades[course_id][student_id] = {"grade": new_grade, "timestamp": now}
                    print_success(f"Grade updated for student {student_id}: {new_grade}")
                else:
                    print_information("Grade update canceled.")
                input("Press enter to continue.")
            else:
                print_error("Error: Grade editing period (7 days) has expired.")
                input("Press enter to continue.")
        else:
            print_error("No grade exists for this student. Please use option 1 (Add Grade) to enter a new grade.")
            input("Press enter to continue.")

    def view_grades(self, instructor, course_id):
        """Displays all grades for a course if the instructor is authorized"""
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to view this course.")
            input("Press enter to continue.")
            return

        if course_id in self.grades:
            print_information(f"\nGrades for {COURSES[course_id]['name']} ({course_id}):")
            for student_id, data in self.grades[course_id].items():
                student_name = STUDENTS[student_id]
                numeric = data["grade"]
                letter = self.convert_to_letter_grade(numeric)
                print_information(f"{student_name} ({student_id}): {numeric} ({letter})")
        else:
            print_warning("No grades have been entered for this course yet.")
        input("Press enter to continue.")

    def convert_to_letter_grade(self, numeric_grade):
        """Converts a numeric grade to a letter grade with +/-"""
        if numeric_grade >= 97:
            return 'A+'
        elif numeric_grade >= 93:
            return 'A'
        elif numeric_grade >= 90:
            return 'A−'
        elif numeric_grade >= 87:
            return 'B+'
        elif numeric_grade >= 83:
            return 'B'
        elif numeric_grade >= 80:
            return 'B−'
        elif numeric_grade >= 77:
            return 'C+'
        elif numeric_grade >= 73:
            return 'C'
        elif numeric_grade >= 70:
            return 'C−'
        elif numeric_grade >= 67:
            return 'D+'
        elif numeric_grade >= 63:
            return 'D'
        elif numeric_grade >= 60:
            return 'D−'
        else:
            return 'F'

    def sort_courses(self, arrangement_type):
        """Sorts course grades in ascending or descending order"""
        if not self.grades:
            print("Grades are empty. Please add a grade")
            input("Press enter to continue.")
            return

        if arrangement_type not in ['a', 'd']:
            print("Please type either (a/d)")
            input("Press enter to continue.")
            return

        if arrangement_type == 'a':
            sorted_grades = {
                course: dict(sorted(students.items(), key=lambda item: item[1]["grade"], reverse=True))
                for course, students in self.grades.items()
            }
            print_success("\nGrades sorted in ascending order!")
        else:  # arrangement_type == 'd'
            sorted_grades = {
                course: dict(sorted(students.items(), key=lambda item: item[1]["grade"]))
                for course, students in self.grades.items()
            }
            print_success("\nGrades sorted in descending order!")

        self.grades = sorted_grades

    def grades_to_edit(self, instructor, course_id):
        """Displays all grades for a course and returns True if grades exist"""
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to view this course.")
            input("Press enter to continue.")
            return False

        if course_id in self.grades:
            print_information(f"\nGrades for {COURSES[course_id]['name']} ({course_id}):")
            for student_id, data in self.grades[course_id].items():
                student_name = STUDENTS[student_id]
                print_information(f"{student_name} ({student_id}): {data['grade']}")
            return True
        else:
            print_warning("No grade exists for this student. Please use option 1 (Add Grade) to enter a new grade.")
            input("Press enter to continue.")
            return False

    def search_student(self, course_id, query):
        """Search for a student by ID or name in the course roster"""
        matches = []
        query_str = str(query).lower()

        try:
            roster = ROSTERS[course_id]
        except KeyError:
            print_error(f"No roster found for course ID: {course_id}")
            return

        for student_id in roster:
            student_name = STUDENTS.get(student_id, "Unknown")
            if query_str in student_name.lower() or query == str(student_id):
                matches.append((student_id, student_name))

        if matches:
            print("\nMatching Students:")
            for sid, name in matches:
                print(f"- {name} (ID: {sid})")
        else:
            print_error("No matching students found.")

    def helper_search_student(self, course_id):
        max_attempts = 3
        attempts = 0
        while attempts < max_attempts:
            answer = input("Would you like to search for students by ID/name? (y/n): ").strip().lower()
            if answer == "y":
                while True:
                    clear_screen()
                    print("========Search Student=========")
                    query = input("Enter Student ID or Name to search (or type 'back' to return): ")
                    if query.lower() == 'back':
                        break
                    self.search_student(course_id, query)
                    input("\nPress enter to continue searching or type 'back' in the next prompt.")
                break  # after search, exit the prompt
            elif answer == "n":
                break
            else:
                attempts += 1
                print_error("Invalid input. Please type 'y' or 'n'.")
        if attempts >= max_attempts:
            print_warning("Too many invalid inputs. Skipping search.")
