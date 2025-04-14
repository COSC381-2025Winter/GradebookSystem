import datetime
from data import COURSES, STUDENTS, ROSTERS
from color_ui import print_success, print_error, print_information, print_warning
from util import clear_screen

class Gradebook:
    def __init__(self):
        # { course_id: { student_id: { "grade": x, "timestamp": datetime } } }
        self.grades = {}

    def add_grade(self, instructor, course_id, student_id, grade, force=False):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to grade this course.")
            input("Press enter to continue.")
            return

        if course_id not in self.grades:
            self.grades[course_id] = {}

        now = datetime.datetime.now()
        if student_id in self.grades[course_id] and not force:
            print_error("Error: Grade already exists. Use 'edit' instead.")
            input("Press enter to continue.")
        else:
            self.grades[course_id][student_id] = {"grade": grade, "timestamp": now}
            name = STUDENTS.get(student_id, f"Student {student_id}")
            print_success(f"Grade added for {name} ({student_id}): {grade}")
            input("Press enter to continue.")

    def edit_grade(self, instructor, course_id, student_id, new_grade):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to edit this course.")
            input("Press enter to continue.")
            return

        course = self.grades.get(course_id, {})
        entry = course.get(student_id)
        if not entry:
            print_error("Error: No existing grade found. Use 'add' instead.")
            input("Press enter to continue.")
            return

        delta = datetime.datetime.now() - entry["timestamp"]
        if delta.days > 7:
            print_error("Error: Grade editing period (7 days) has expired.")
            input("Press enter to continue.")
            return

        now = datetime.datetime.now()
        self.grades[course_id][student_id] = {"grade": new_grade, "timestamp": now}
        name = STUDENTS.get(student_id, f"Student {student_id}")
        print_success(f"Grade updated for {name} ({student_id}): {new_grade}")
        input("Press enter to continue.")

    def view_grades(self, instructor, course_id):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to view this course.")
            input("Press enter to continue.")
            return

        course = self.grades.get(course_id)
        if not course:
            print_warning("No grades have been entered for this course yet.")
            input("Press enter to continue.")
            return

        print_information(f"\nGrades for {COURSES[course_id]['name']} ({course_id}):")
        for sid, data in course.items():
            name = STUDENTS.get(sid, f"Student {sid}")
            print_information(f"{name} ({sid}): {data['grade']}")
        input("Press enter to continue.")

    def sort_courses(self, arrangement_type):
        if not self.grades:
            print_warning("Grades are empty. Please add a grade")
            input("Press enter to continue.")
            return

        if arrangement_type not in ('a','d'):
            print_warning("Please type either (a/d)")
            input("Press enter to continue.")
            return

        reverse = (arrangement_type == 'a')
        for course, students in self.grades.items():
            self.grades[course] = dict(
                sorted(students.items(), key=lambda kv: kv[1]["grade"], reverse=reverse)
            )

    def search_student(self, course_id, query):
        matches = []
        q = str(query).lower()
        for sid in ROSTERS.get(course_id, []):
            name = STUDENTS.get(sid, "Unknown")
            if q in name.lower() or q == str(sid):
                matches.append((sid, name))

        if matches:
            print_information("\nMatching Students:")
            for sid, name in matches:
                print_information(f"- {name} (ID: {sid})")
        else:
            print_warning("No matching students found.")

    def helper_search_student(self, course_id):
        while True:
            ans = input("Search students by ID/name? (y/n): ").strip().lower()
            if ans == 'y':
                clear_screen()
                print_information("======== Search Student ========")
                query = input("Enter Student ID or Name (or 'back'): ")
                if query.lower() == 'back':
                    return
                self.search_student(course_id, query)
                input("Press enter to continue.")
            elif ans == 'n':
                return
            else:
                print_error("Invalid input; please enter 'y' or 'n'.")

    def add_student(self, instructor, course_id):
        """Add a new student to the roster with an optional initial grade."""
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to add students.")
            input("Press enter to continue.")
            return

        sid = input("Enter new Student ID: ").strip()
        if not sid.isnumeric():
            print_error("Error: Student ID must be numeric.")
            input("Press enter to continue.")
            return
        sid = int(sid)
        ROSTERS.setdefault(course_id, []).append(sid)

        grade = input("Enter initial grade (or leave blank for 0): ").strip()
        grade_val = float(grade) if grade.replace('.','',1).isdigit() else 0.0
        self.add_grade(instructor, course_id, sid, grade_val, force=True)

