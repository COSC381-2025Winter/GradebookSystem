import sys
import datetime
from data import COURSES, STUDENTS, ROSTERS
from color_ui import print_success, print_error, print_information, print_warning
from util import clear_screen as real_clear_screen

# Define a wrapper for clear_screen: only clear if stdout is a tty.
def clear_screen():
    if sys.stdout.isatty():
        real_clear_screen()
    # Otherwise, do nothing

def _wait_for_continue():
    # For testing purposes, do nothing.
    pass

class Gradebook:
    def __init__(self):
        # Grades structure: { course_id: { student_id: { "grade": x, "timestamp": datetime } } }
        self.grades = {}

    def grades_to_edit(self, instructor, course_id):
        return self.grades.get(course_id, {})

    def add_grade(self, instructor, course_id, student_id, grade, force=False):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to grade this course.")
            _wait_for_continue()
            return

        if course_id not in self.grades:
            self.grades[course_id] = {}

        now = datetime.datetime.now()
        if student_id in self.grades[course_id] and not force:
            print_error("Error: Grade already exists. Use 'edit' instead.")
            _wait_for_continue()
        else:
            self.grades[course_id][student_id] = {"grade": grade, "timestamp": now}
            # Look up student name; if not found, use lowercase fallback.
            name = STUDENTS.get(student_id)
            if not name:
                name = f"student {student_id}"
            print_success(f"Grade added for {name} ({student_id}): {grade}")
            _wait_for_continue()

    def edit_grade(self, instructor, course_id, student_id, new_grade):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to edit this course.")
            _wait_for_continue()
            return

        course = self.grades.get(course_id, {})
        entry = course.get(student_id)
        if not entry:
            print_error("Error: No existing grade found. Use 'add' instead.")
            _wait_for_continue()
            return

        delta = datetime.datetime.now() - entry["timestamp"]
        if delta.days > 7:
            print_error("Error: Grade editing period (7 days) has expired.")
            _wait_for_continue()
            return

        now = datetime.datetime.now()
        self.grades[course_id][student_id] = {"grade": new_grade, "timestamp": now}
        name = STUDENTS.get(student_id)
        if not name:
            name = f"student {student_id}"
        print_success(f"Grade updated for {name} ({student_id}): {new_grade}")
        _wait_for_continue()

    def view_grades(self, instructor, course_id):
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to view this course.")
            _wait_for_continue()
            return "Access Denied"
        course = self.grades.get(course_id)
        if not course:
            print_warning("No grades have been entered for this course yet.")
            _wait_for_continue()
            return None
        print_information(f"\nGrades for {COURSES[course_id]['name']} ({course_id}):")
        for sid, data in course.items():
            name = STUDENTS.get(sid)
            if not name:
                name = f"student {sid}"
            print_information(f"{name} ({sid}): {data['grade']}")
        _wait_for_continue()
        return course

    def sort_courses(self, arrangement_type):
        if not self.grades:
            print_warning("Grades are empty. Please add a grade")
            _wait_for_continue()
            return

        if arrangement_type not in ('a', 'd'):
            print_warning("Please type either (a/d)")
            _wait_for_continue()
            return

        reverse = (arrangement_type == 'a')
        for course, students in self.grades.items():
            self.grades[course] = dict(
                sorted(students.items(), key=lambda kv: kv[1]["grade"], reverse=reverse)
            )
        _wait_for_continue()

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
            ans = str(input("Search students by ID/name? (y/n): ")).strip().lower()
            if ans == 'y':
                clear_screen()
                print_information("======== Search Student ========")
                query = input("Enter Student ID or Name (or 'back'): ")
                if str(query).strip().lower() == 'back':
                    return
                self.search_student(course_id, query)
                _wait_for_continue()
            elif ans == 'n':
                return
            else:
                print_error("Invalid input; please enter 'y' or 'n'.")
