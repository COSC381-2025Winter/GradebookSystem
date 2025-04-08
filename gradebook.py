import datetime
from data import COURSES, STUDENTS, ROSTERS
from color_ui import print_success, print_error, print_information, print_warning

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
            print_error("Error: Grade already exists. Use 'edit' instead.")
            input("Press enter to continue.")
        else:
            self.grades[course_id][student_id] = {"grade": grade, "timestamp": now}
            print_success(f"Grade added for student {student_id}: {grade}")
            input("Press enter to continue.")

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
            old_timestamp = self.grades[course_id][student_id]["timestamp"]
            now = datetime.datetime.now()
            delta = now - old_timestamp

            if delta.days <= 7:
                self.grades[course_id][student_id] = {"grade": new_grade, "timestamp": now}
                print_success(f"Grade updated for student {student_id}: {new_grade}")
                input("Press enter to continue.")
            else:
                print_error("Error: Grade editing period (7 days) has expired.")
                input("Press enter to continue.")
        else:
            print_error("Error: No existing grade found. Use 'add' instead.")
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
