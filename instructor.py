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

    def display_courses(self):
        themed_print = print_success if self.get_theme() == "dark" else print_information
        themed_print(f"\nCourses for {self.name}:")
        for cid, cname in self.courses.items():
            themed_print(f"{cid}: {cname}")

    # Theme management passthroughs
    def set_theme(self, theme):
        self.color_theme.set_theme(theme)

    def get_theme(self):
        return self.color_theme.get_theme()