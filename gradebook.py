import datetime
from data import COURSES, STUDENTS, ROSTERS
from color_ui import print_success, print_error, print_information, print_warning

class Gradebook:
    def __init__(self):
        # Grades are stored as: {course_id: {student_id: {"grade": value, "timestamp": datetime_obj}}}
        self.grades = {}

    def add_grade(self, instructor, course_id, student_id, grade, force=False):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to grade this course.")
            return "Access Denied"

        if course_id not in self.grades:
            self.grades[course_id] = {}

        now = datetime.datetime.now()

        if student_id in self.grades[course_id] and not force:
            print_error("Error: Grade already exists. Use 'edit' instead.")
            return "Grade already exists"
        else:
            self.grades[course_id][student_id] = {"grade": grade, "timestamp": now}
            print_success(f"Grade added for student {student_id}: {grade}")
            return "Grade added"

    def edit_grade(self, instructor, course_id, student_id, new_grade):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to edit this course.")
            return "Access Denied"

        if course_id in self.grades and student_id in self.grades[course_id]:
            old_timestamp = self.grades[course_id][student_id]["timestamp"]
            now = datetime.datetime.now()
            if (now - old_timestamp).days <= 7:
                self.grades[course_id][student_id] = {"grade": new_grade, "timestamp": now}
                print_success(f"Grade updated for student {student_id}: {new_grade}")
                return "Grade updated"
            else:
                print_error("Error: Grade editing period (7 days) has expired.")
                return "Edit window expired"
        else:
            print_error("Error: No existing grade found. Use 'add' instead.")
            return "No existing grade"

    def view_grades(self, instructor, course_id):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to view this course.")
            return "Access Denied"

        if course_id in self.grades:
            print_information(f"\nGrades for {COURSES[course_id]['name']} ({course_id}):")
            for student_id, data in self.grades[course_id].items():
                student_name = STUDENTS.get(student_id, f"Student {student_id}")
                print_information(f"{student_name} ({student_id}): {data['grade']}")
            return self.grades[course_id]
        else:
            print_warning("No grades have been entered for this course yet.")
            return {}

    def sort_courses(self, arrangement_type):
        if not self.grades:
            print("Grades are empty. Please add a grade")
            return

        if arrangement_type not in ['a', 'd']:
            print("Please type either (a/d)")
            return

        # For descending order
        if arrangement_type == 'd':
            sorted_grades = {
                course: dict(sorted(students.items(), key=lambda item: item[1]["grade"]))
                for course, students in self.grades.items()
            }
        # For ascending order (reverse sorted)
        elif arrangement_type == 'a':
            sorted_grades = {
                course: dict(sorted(students.items(), key=lambda item: item[1]["grade"], reverse=True))
                for course, students in self.grades.items()
            }
        self.grades = sorted_grades

    def grades_to_edit(self, instructor, course_id):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to view this course.")
            return False

        if course_id in self.grades:
            print_information(f"\nGrades for {COURSES[course_id]['name']} ({course_id}):")
            for student_id, data in self.grades[course_id].items():
                student_name = STUDENTS[student_id]
                print_information(f"{student_name} ({student_id}): {data['grade']}")
            return True
        else:
            print_warning("No grades have been entered for this course yet. Use 'add' instead")
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
        # Note: This helper remains interactive.
        answer = True
        while answer:
            answer = input("Would you like to search for students by ID/name?(y/n): ")
            if answer.lower() == "y":
                answer = False
                while True:
                    # In interactive mode, clear the screen before a search
                    # (Assuming clear_screen is an imported utility)
                    from util import clear_screen
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
