import datetime
from data import INSTRUCTORS, COURSES
from color_theme import ColorTheme
from color_ui import print_information, print_success

class Instructor:
    def __init__(self, instructor_id):
        self.color_theme = ColorTheme("light")
        self.instructor_id = instructor_id
        self.name = INSTRUCTORS.get(instructor_id)
        self.courses = {}

        # Assign courses if instructor exists
        if self.name:
            self._load_courses()

    def _load_courses(self):
        for course_id, course in COURSES.items():
            if course['instructor_id'] == self.instructor_id:
                self.courses[course_id] = course['name']

    def is_authenticated(self):
        return self.name is not None

    def has_access(self, course_id):
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

        themed_print = print_success if self.get_theme() == "dark" else print_information
        themed_print(f"\nCourses for {self.name}:")
        for cid, cname in self.courses.items():
            themed_print(f"{cid}: {cname}")

    # Theme management passthroughs
    def set_theme(self, theme):
        self.color_theme.set_theme(theme)

    def get_theme(self):
        return self.color_theme.get_theme()
>>>>>>> origin/main
import datetime
from data import INSTRUCTORS, COURSES
from color_theme import ColorTheme
from color_ui import print_information, print_success

class Instructor:
    def __init__(self, instructor_id):
        self.color_theme = ColorTheme("light")
        self.instructor_id = instructor_id
        self.name = INSTRUCTORS.get(instructor_id)
        self.courses = {}

        # Assign courses if instructor exists
        if self.name:
            self._load_courses()

    def _load_courses(self):
        for course_id, course in COURSES.items():
            if course['instructor_id'] == self.instructor_id:
                self.courses[course_id] = course['name']

    def is_authenticated(self):
        return self.name is not None

    def has_access(self, course_id):
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
        """Displays the current semester and courses taught by the instructor, respecting theme."""
        themed_print = print_success if self.get_theme() == "dark" else print_information
        current_semester = self.get_current_semester()
        current_year = datetime.datetime.now().year
        themed_print(f"\n{current_semester} {current_year}") # Print semester and year first
        themed_print(f"Welcome {self.name}! Your courses:") # Then print welcome message
        for cid, cname in self.courses.items():
            themed_print(f"- {cname} ({cid})") # Use HEAD formatting

    # Theme management passthroughs
    def set_theme(self, theme):
        self.color_theme.set_theme(theme)

    def get_theme(self):
        return self.color_theme.get_theme()
=======
        themed_print = print_success if self.get_theme() == "dark" else print_information
        themed_print(f"\nCourses for {self.name}:")
        for cid, cname in self.courses.items():
            themed_print(f"{cid}: {cname}")

    # Theme management passthroughs
    def set_theme(self, theme):
        self.color_theme.set_theme(theme)

    def get_theme(self):
        return self.color_theme.get_theme()
>>>>>>> origin/main
