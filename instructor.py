import datetime
import os
import re
from data import INSTRUCTORS, COURSES
from color_theme import ColorTheme
from color_ui import print_information, print_success
from data import INSTRUCTORS
from credentials import PASSWORDS

class Instructor:
    def __init__(self, instructor_id):
        self.color_theme = ColorTheme("light")  # Default to light theme
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
        # Ensure course_id is compared consistently (e.g., uppercase)
        return course_id.upper() in self.courses

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
        themed_print(f"\n{current_semester} {current_year}")  # Print semester and year first
        themed_print(f"Welcome {self.name}! Your courses:")  # Then print welcome message
        for cid, cname in self.courses.items():
            print_information(f"- {cname} ({cid})")
            themed_print(f"- {cname} ({cid})") # Use formatting from winter_semester branch

    # Theme management passthroughs
    def set_theme(self, theme):
        self.color_theme.set_theme(theme)

    def get_theme(self):
        return self.color_theme.get_theme()

    def get_course_code_by_name(self,course_name):
    # Iterate through the dictionary to find the course with the given name
        sucess=False
        for course_code, course_info in COURSES.items():
            if course_name.lower() in course_info["name"].lower():  # ignores cases when searching
             sucess =True
             break
        if sucess:
            return course_code # returns the course code
        
        return course_name
    
    @staticmethod
    def add_instructor(name, password):
        from data import INSTRUCTORS
        from credentials import PASSWORDS

        # Generate new unique ID
        new_id = max(INSTRUCTORS.keys()) + 1 if INSTRUCTORS else 101
        INSTRUCTORS[new_id] = name
        PASSWORDS[new_id] = password

        # Read the entire data.py to get all content
        with open("data.py", "r") as f:
            lines = f.readlines()

        # Prepare the new INSTRUCTORS block
        new_instructors_block = "INSTRUCTORS = {\n"
        for iid, iname in INSTRUCTORS.items():
            new_instructors_block += f"    {iid}: \"{iname}\",\n"
        new_instructors_block += "}\n"

        # Write back to data.py, replacing the INSTRUCTORS block
        with open("data.py", "w") as f:
            in_instructors_block = False
            for line in lines:
                if line.strip().startswith("INSTRUCTORS = {"):
                    # Start of INSTRUCTORS block, write new block and skip old block
                    f.write(new_instructors_block)
                    in_instructors_block = True
                elif in_instructors_block and line.strip() == "}":
                    # End of old INSTRUCTORS block, skip this line
                    in_instructors_block = False
                elif not in_instructors_block:
                    # Write all other lines as is
                    f.write(line)

            # If no INSTRUCTORS block was found, append the new block
            if not any(line.strip().startswith("INSTRUCTORS = {") for line in lines):
                f.write("\n" + new_instructors_block)

        # Write the updated PASSWORDS to credentials.py
        with open("credentials.py", "w") as f:
            f.write("PASSWORDS = {\n")
            for iid, pw in PASSWORDS.items():
                f.write(f"    {iid}: \"{pw}\",\n")
            f.write("}\n")

        return new_id

       
            
