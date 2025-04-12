import datetime
from data import COURSES, STUDENTS, ROSTERS
from color_ui import print_success, print_error, print_information, print_warning

class Gradebook:
    def __init__(self):
        self.grades = {}  # {course_id: {student_id: {"grade": x, "timestamp": y}}}
        self.grade_history = {}  # {course_id: {student_id: [{"grade": "A", "timestamp": datetime1}, ...]}}

    def add_grade(self, instructor, course_id, student_id, grade):
        """Adds a grade for a student in a specific course"""
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to grade this course.")
            input("Press enter to continue.")
            return

        if course_id not in self.grades:
            self.grades[course_id] = {}
            
        # Initialize grade history if not exists
        if course_id not in self.grade_history:
            self.grade_history[course_id] = {}
        if student_id not in self.grade_history[course_id]:
            self.grade_history[course_id][student_id] = []

        now = datetime.datetime.now()

        if student_id in self.grades[course_id]:
            print_error("Error: Grade already exists. Use 'edit' instead.")
            input("Press enter to continue.")
        else:
            self.grades[course_id][student_id] = {"grade": grade, "timestamp": now}
            # Add to history
            self.grade_history[course_id][student_id].append({"grade": grade, "timestamp": now})
            print_success(f"Grade added for student {student_id}: {grade}")
            input("Press enter to continue.")

    def edit_grade(self, instructor, course_id, student_id, new_grade):
        """Edits an existing grade but only within 7 days of the first entry"""
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
                
                # Initialize grade history if not exists
                if course_id not in self.grade_history:
                    self.grade_history[course_id] = {}
                if student_id not in self.grade_history[course_id]:
                    self.grade_history[course_id][student_id] = []
                
                # Add to history
                self.grade_history[course_id][student_id].append({"grade": new_grade, "timestamp": now})
                
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
                print_information(f"{student_name} ({student_id}): {data['grade']}")
        else:
            print_warning("No grades have been entered for this course yet.")
        
        input("Press enter to continue.")
        
    def view_grade_history(self, instructor, course_id, student_id):
        """Displays the grade history for a specific student in a course"""
        if not instructor.has_access(course_id):
            print_error("Access Denied: You are not authorized to view this course's history.")
            input("Press enter to continue.")
            return
            
        if student_id not in STUDENTS:
            print_error(f"Student ID {student_id} not found.")
            input("Press enter to continue.")
            return
            
        if course_id not in self.grade_history or student_id not in self.grade_history[course_id]:
            print_warning(f"No grade history found for student {student_id} in this course.")
            input("Press enter to continue.")
            return
            
        history = self.grade_history[course_id][student_id]
        student_name = STUDENTS[student_id]
        
        print_information(f"\nGrade History for {student_name} ({student_id}) in {COURSES[course_id]['name']} ({course_id}):")
        for i, entry in enumerate(history, 1):
            timestamp_str = entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            print_information(f"{i}. Grade: {entry['grade']}, Date: {timestamp_str}")
            
        input("Press enter to continue.")