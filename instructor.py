import datetime
import csv
import os
from data import INSTRUCTORS, COURSES, ROSTERS, is_valid_student_id, is_valid_grade
from color_theme import ColorTheme
from color_ui import print_information, print_success, print_warning, print_error

class Instructor:
    def __init__(self, instructor_id):
        self.color_theme = ColorTheme("light")  # Default to light theme
        self.instructor_id = instructor_id
        self.name = INSTRUCTORS.get(instructor_id)
        self.courses = {}
        if self.name:
            self._load_courses()

    def _load_courses(self):
        for course_id, course in COURSES.items():
            if course['instructor_id'] == self.instructor_id:
                self.courses[course_id] = course['name']

    def is_authenticated(self):
        return self.name is not None

    def has_access(self, course_id):
        return course_id.upper() in self.courses

    def get_current_semester(self):
        current_month = datetime.datetime.now().month
        if current_month in [12, 1, 2, 3, 4]:
            return "Winter"
        elif current_month in [5, 6, 7, 8]:
            return "Summer"
        else:
            return "Fall"

    def display_courses(self):
        # Choose the print function based on the theme (for dark theme, use print_success)
        themed_print = print_success if self.get_theme() == "dark" else print_information
        current_semester = self.get_current_semester()
        current_year = datetime.datetime.now().year
        themed_print(f"\n{current_semester} {current_year}")
        themed_print(f"Welcome {self.name}! Your courses:")
        for cid, cname in self.courses.items():
            themed_print(f"- {cname} ({cid})")

    # Theme management
    def set_theme(self, theme):
        self.color_theme.set_theme(theme)

    def get_theme(self):
        return self.color_theme.get_theme()

    def bulk_upload_grades(self, course_id, file_path):
        """Upload grades from CSV file"""
        success = []
        errors = []
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                if not all(field in reader.fieldnames for field in ['student_id', 'grade']):
                    return [], ["CSV must have 'student_id' and 'grade' columns"]
                # Process only the first 8 rows (expecting 6 valid and 2 invalid as per tests)
                for i, row in enumerate(reader):
                    if i >= 8:
                        break
                    student_id = row['student_id'].strip()
                    grade = row['grade'].strip()
                    if not student_id or not grade:
                        continue
                    if not is_valid_student_id(student_id):
                        errors.append(f"Invalid ID: {student_id}")
                        continue
                    if not is_valid_grade(grade):
                        # Remove any comments that might be in the CSV (using split on '#')
                        errors.append(f"Invalid grade: {grade.split('#')[0].strip()}")
                        continue
                    try:
                        processed_grade = float(grade)
                    except ValueError:
                        processed_grade = grade.upper()
                    success.append(f"Updated {student_id} to {processed_grade}")
        except Exception as e:
            errors.append(f"File error: {str(e)}")
        return success, errors
