import datetime
from data import COURSES, STUDENTS, ROSTERS
from util import clear_screen

class Gradebook:
    def __init__(self):
        # grades: {course_id: {student_id: {"grade": x, "timestamp": y}}}
        self.grades = {}

    def add_grade(self, instructor, course_id, student_id, grade, force=False):
        """
        Adds a grade for a student in a specific course.
        Returns a status string for testing.
        """
        if not instructor.has_access(course_id):
            return "Access Denied"

        if course_id not in self.grades:
            self.grades[course_id] = {}

        now = datetime.datetime.now()
        if student_id in self.grades[course_id] and not force:
            return "Grade already exists"

        self.grades[course_id][student_id] = {"grade": grade, "timestamp": now}
        return "Grade added"

    def edit_grade(self, instructor, course_id, student_id, new_grade):
        """
        Edits an existing grade within 7 days of the original entry.
        Returns a status string for testing.
        """
        if not instructor.has_access(course_id):
            return "Access Denied"

        if course_id in self.grades and student_id in self.grades[course_id]:
            old_timestamp = self.grades[course_id][student_id]["timestamp"]
            now = datetime.datetime.now()
            if (now - old_timestamp).days <= 7:
                self.grades[course_id][student_id] = {"grade": new_grade, "timestamp": now}
                return "Grade updated"
            else:
                return "Edit window expired"
        else:
            return "No existing grade"

    def view_grades(self, instructor, course_id):
        """
        Returns the grades dict for a course or an access error string.
        """
        if not instructor.has_access(course_id):
            return "Access Denied"
        return self.grades.get(course_id, {})

    def search_student(self, course_id, query):
        """Search for a student by ID or name in the course roster"""
        matches = []
        query_str = str(query).lower()
        for student_id in ROSTERS.get(course_id, []):
            student_name = STUDENTS.get(student_id, "Unknown")
            if query_str in student_name.lower() or query_str == str(student_id):
                matches.append((student_id, student_name))
        if matches:
            return [f"- {name} (ID: {sid})" for sid, name in matches]
        else:
            return []

    def helper_search_student(self, course_id):
        """Interactive helper to search for students before grading"""
        while True:
            answer = input("Would you like to search for students by ID/name?(y/n): ")
            if answer.lower() == 'y':
                while True:
                    clear_screen()
                    print("========Search Student=========")
                    query = input("Enter Student ID or Name to search (or type 'back' to return): ")
                    if query.lower() == 'back':
                        break
                    results = self.search_student(course_id, query)
                    if results:
                        for line in results:
                            print(line)
                    else:
                        print("No matching students found.")
                    cont = input("\nPress enter to continue searching or type 'back' in the next prompt.")
                    if cont.lower() == 'back':
                        break
                break
            elif answer.lower() == 'n':
                break
            else:
                print("invalid input")

    def sort_courses(self, order):
        """Sorts each course's grades by grade value.
        'a' for ascending, 'd' for descending.
        Returns the updated grades dict or an error string.
        """
        if not self.grades:
            return "No grades to sort"
        if order not in ('a', 'd'):
            return "Invalid sort order"
        sorted_grades = {}
        for cid, students in self.grades.items():
            reverse = (order == 'd')
            sorted_items = sorted(students.items(), key=lambda item: item[1]['grade'], reverse=reverse)
            sorted_grades[cid] = dict(sorted_items)
        self.grades = sorted_grades
        return self.grades
