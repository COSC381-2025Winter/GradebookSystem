from data import INSTRUCTORS, COURSES

class Instructor:
    def __init__(self, instructor_id):
        # Save ID and look up name
        self.instructor_id = instructor_id
        self.name = INSTRUCTORS.get(instructor_id)
        # Default theme
        self.theme = "light"
        # Build a dict of courses taught by this instructor
        self.courses = {
            cid: info["name"]
            for cid, info in COURSES.items()
            if info.get("instructor_id") == instructor_id
        }

    def is_authenticated(self):
        return self.name is not None

    def has_access(self, course_id):
        return course_id in self.courses

    def display_courses(self):
        """
        Prints the list of course IDs this instructor teaches.
        """
        for cid in self.courses:
            print(cid)

    def set_theme(self, theme):
        """
        Sets the instructor's display theme. Only 'light' or 'dark' are valid.
        """
        if theme not in ("light", "dark"):
            raise ValueError(f"Invalid theme: {theme}")
        self.theme = theme

    def get_theme(self):
        """
        Returns the current display theme.
        """
        return self.theme
