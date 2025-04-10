from data import INSTRUCTORS, COURSES

class Instructor:
    def __init__(self, instructor_id):
        self.color_theme = "light"  # Default theme is light
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
        print(f"\nWelcome {self.name}! Your courses:")
        for cid, cname in self.courses.items():
            print(f"- {cname} ({cid})")

    def get_theme(self):
        """Gets the current color theme of the instructor."""
        return self.color_theme

    def set_theme(self, theme):
        """Allows the instructor to set their preferred color theme."""
        if theme not in ["light", "dark"]:
            raise ValueError(f"Invalid theme '{theme}'. Choose 'light' or 'dark'.")
        self.color_theme = theme