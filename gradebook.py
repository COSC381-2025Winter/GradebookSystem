import datetime
from data import COURSES, STUDENTS, ROSTERS

class Gradebook:
    def __init__(self):
        self.grades = {}  # {course_id: {student_id: {"grade": x, "timestamp": y}}}

    def add_grade(self, instructor, course_id, student_id, grade):
        """Adds a grade for a student in a specific course"""
        if not instructor.has_access(course_id):
            input("Access Denied: You are not authorized to grade this course. Press enter to continue.")
            return

        if course_id not in self.grades:
            self.grades[course_id] = {}

        now = datetime.datetime.now()

        if student_id in self.grades[course_id]:
            input("Error: Grade already exists. Use 'edit' instead. Press enter to continue.")
        else:
            self.grades[course_id][student_id] = {"grade": grade, "timestamp": now}
            input(f"Grade added for student {student_id}: {grade}. Press enter to continue.")

    def edit_grade(self, instructor, course_id, student_id, new_grade):
        """Edits an existing grade but only within 7 days of the first entry"""
        if not instructor.has_access(course_id):
            input("Access Denied: You are not authorized to edit this course. Press enter to continue.")
            return

        if course_id in self.grades and student_id in self.grades[course_id]:
            old_timestamp = self.grades[course_id][student_id]["timestamp"]
            now = datetime.datetime.now()
            delta = now - old_timestamp

            if delta.days <= 7:
                self.grades[course_id][student_id] = {"grade": new_grade, "timestamp": now}
                input(f"Grade updated for student {student_id}: {new_grade}. Press enter to continue.")
            else:
                input("Error: Grade editing period (7 days) has expired. Press enter to continue.")
        else:
            input("Error: No existing grade found. Use 'add' instead. Press enter to continue.")

    def view_grades(self, instructor, course_id):
        """Displays all grades for a course if the instructor is authorized"""
        if not instructor.has_access(course_id):
            input("Access Denied: You are not authorized to view this course. Press enter to continue.")
            return

        if course_id in self.grades:
            print(f"\nGrades for {COURSES[course_id]['name']} ({course_id}):")
            for student_id, data in self.grades[course_id].items():
                student_name = STUDENTS[student_id]
                print(f"{student_name} ({student_id}): {data['grade']}")
        else:
            print("No grades have been entered for this course yet.")
        
        input("Press enter to continue.")