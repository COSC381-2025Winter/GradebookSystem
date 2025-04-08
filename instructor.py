import datetime
from data import INSTRUCTORS, COURSES
from color_ui import print_information

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

    def get_current_semester(self):
        """Determines the current semester based on the month."""
        current_month = datetime.datetime.now().month
        if current_month in [12, 1, 2, 3, 4]:
            return "Winter"
        elif current_month in [5, 6, 7, 8]:
            return "Summer"
        else:  # Months 9, 10, 11
            return "Fall"

    def display_courses(self):
        """Displays the current semester and courses taught by the instructor."""
        current_semester = self.get_current_semester()
        current_year = datetime.datetime.now().year
        print_information(f"\n{current_semester} {current_year}") # Print semester and year first
        print_information(f"Welcome {self.name}! Your courses:") # Then print welcome message
        for cid, cname in self.courses.items():
            print_information(f"- {cname} ({cid})")
