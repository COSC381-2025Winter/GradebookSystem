from data import INSTRUCTORS, COURSES
import os
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

    def get_Instructors():
        return INSTRUCTORS

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

    @staticmethod
    def add_instructor(name):
        with open()

        new_id = max(INSTRUCTORS.keys()) + 1
        INSTRUCTORS[new_id]= name
        return new_id            
    
