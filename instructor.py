from data import INSTRUCTORS, COURSES

class Instructor:
    def __init__(self, instructor_id):
        self.instructor_id = instructor_id
        self.name = INSTRUCTORS.get(instructor_id)
        # Build courses dictionary using the course ID as key and name as value.
        self.courses = {
            cid: COURSES[cid]["name"]
            for cid in COURSES
            if COURSES[cid]["instructor_id"] == instructor_id
        }
        self.theme = "light"  # Default theme

    def is_authenticated(self):
        return self.name is not None

    def has_access(self, course_id):
        # Assume course IDs are provided in uppercase.
        return course_id in self.courses

    def display_courses(self):
        # For non-interactive testing, simply return the list of course IDs.
        return list(self.courses.keys())

    def set_theme(self, theme):
        self.theme = theme

    def get_theme(self):
        return self.theme
