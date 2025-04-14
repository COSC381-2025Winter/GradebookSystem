import datetime
from data import COURSES, STUDENTS, ROSTERS

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
            delta = now - old_timestamp

            if delta.days <= 7:
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
            output = [f"- {name} (ID: {sid})" for sid, name in matches]
            return output
        else:
            return []
