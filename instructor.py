from data import INSTRUCTORS, COURSES
from color_ui import print_information
import csv
from data import is_valid_student_id, is_valid_grade

class Instructor:
    def __init__(self, instructor_id):
        if instructor_id in INSTRUCTORS:
            self.instructor_id = instructor_id
            self.name = INSTRUCTORS[instructor_id]
            self.courses = self.get_courses()
        else:
            self.instructor_id = None
            self.name = None
            self.courses = []

    def get_courses(self):
        """Returns the list of courses assigned to the instructor."""
        return {cid: COURSES[cid]["name"] for cid in COURSES if COURSES[cid]["instructor_id"] == self.instructor_id}

    def is_authenticated(self):
        """Checks if the instructor authentication was successful."""
        return self.instructor_id is not None

    def has_access(self, course_id):
        """Checks if the instructor has access to the given course."""
        return course_id in self.courses

    def display_courses(self):
        """Displays courses taught by the instructor."""
        print_information(f"\nWelcome {self.name}! Your courses:")
        for cid, cname in self.courses.items():
            print_information(f"- {cname} ({cid})")

    def bulk_upload_grades(self, course_id, file_path):
        """Upload grades from CSV file"""
        success = []
        errors = []
        
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                if not all(field in reader.fieldnames for field in ['student_id', 'grade']):
                    return [], ["CSV must have 'student_id' and 'grade' columns"]
                
                for row in reader:
                    student_id = row['student_id'].strip()
                    grade = row['grade'].strip().upper()
                    
                    if not is_valid_student_id(student_id):
                        errors.append(f"Invalid ID: {student_id}")
                        continue
                        
                    if not is_valid_grade(grade):
                        errors.append(f"Invalid grade: {grade}")
                        continue
                    
                    # If we get here, it's valid!
                    success.append(f"Updated {student_id} to {grade}")
                    
        except Exception as e:
            errors.append(f"File error: {str(e)}")
        
        return success, errors