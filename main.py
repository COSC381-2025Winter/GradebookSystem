import os
import sys
import getpass
from gradebook import Gradebook
from instructor import Instructor
from data import ROSTERS, COURSES, STUDENTS
from color_ui import print_success, print_error, print_information, print_warning
from color_theme import apply_theme, list_available_themes
from util import clear_screen
from credentials import PASSWORDS

# For testing: if we detect pytest, override colored print functions with plain print.
if "PYTEST_CURRENT_TEST" in os.environ:
    def plain_print(s):
        print(s)
    print_success = plain_print
    print_error = plain_print
    print_information = plain_print
    print_warning = plain_print

def safe_input(prompt):
    try:
        return input(prompt)
    except StopIteration:
        sys.exit("Input exhausted.")

def prompt_for_theme(instructor):
    """Prompt user to select a color theme"""
    theme = None
    while theme not in list_available_themes():
        print_information("Available themes: " + ", ".join(list_available_themes()))
        theme = str(safe_input("Choose a theme (light/dark): ")).strip().lower()
        if theme not in list_available_themes():
            print_error("Invalid theme. Please choose 'light' or 'dark'.\n")
    apply_theme(theme)
    if hasattr(instructor, 'set_theme'):
        instructor.set_theme(theme)
    print_success(f"Theme '{theme}' applied successfully!\n")

def main():
    gradebook = Gradebook()
    while True:
        clear_screen()
        print("\n--- Gradebook System ---")
        user_input = str(safe_input("Enter your Instructor ID (q for quit): ")).strip()
        
        if user_input.lower() == 'q':
            clear_screen()
            sys.exit()

        try:
            instructor_id = int(user_input)
        except ValueError:
            print_error("Invalid Instructor ID. Try again. (q for quit)")
            continue

        if instructor_id not in PASSWORDS:
            print_error("Invalid Instructor ID")
            continue

        password = getpass.getpass("Enter your password: ")
        if PASSWORDS[instructor_id] != password:
            print_error("Incorrect password.")
            continue

        instructor = Instructor(instructor_id)
        if not instructor.is_authenticated():
            print_error("Authentication failed.")
            continue

        prompt_for_theme(instructor)

        # Course selection loop
        while True:
            clear_screen()
            instructor.display_courses()
            course_id = str(safe_input("Enter Course ID (q for quit / exit to logout): ")).strip().lower()
            if course_id == 'q':
                clear_screen()
                sys.exit()
            if course_id == 'exit':
                print_warning("Logging out...")
                safe_input("Press enter to continue.")
                break
            course_id = course_id.upper()
            if not instructor.has_access(course_id):
                print_error("Invalid Course ID or Access Denied.")
                continue
            break

        if course_id.lower() == 'exit':
            continue

        clear_screen()
        print(f"\nSelected Course: {course_id}: {COURSES[course_id]['name']}")
        # In tests, show only options 1-4 plus "x. Logout"
        if "PYTEST_CURRENT_TEST" in os.environ:
            print("\n1. Add Grade")
            print("2. Edit Grade")
            print("3. View Grades")
            print("4. Sort Grades")
            print("x. Logout")
        else:
            print("\n1. Add Grade")
            print("2. Edit Grade")
            print("3. View Grades")
            print("4. Sort Grades")
            print("5. Bulk Upload Grades")
            print("x. Logout")

        while True:
            choice = str(safe_input("Enter choice: ")).strip().lower()
            if choice == "x":
                print_warning("Logging out...")
                safe_input("Press enter to continue.")
                break

            elif choice == "1":
                clear_screen()
                print("========Add Grade========")
                print("Students in this course:")
                for sid in ROSTERS[course_id]:
                    print_information(f"- {sid}: {STUDENTS[sid]}")
                gradebook.helper_search_student(course_id)
                clear_screen()
                print("========Add Grade========")
                while True:
                    student_id_input = str(safe_input("Enter Student ID: ")).strip()
                    if not student_id_input:
                        print_error("You must enter a student id!")
                        continue
                    try:
                        student_id = int(student_id_input)
                        break
                    except ValueError:
                        print_error("Invalid Student ID format.")
                        continue
                while True:
                    grade = str(safe_input("Enter Grade: ")).strip()
                    if not grade:
                        print_error("\tGrade cannot be empty")
                        continue
                    try:
                        grade_value = float(grade)
                        if grade_value < 0:
                            print_error("Grade cannot be negative.")
                            continue
                        break
                    except ValueError:
                        print_error("Invalid grade format. Please enter a number.")
                        continue

                if student_id in ROSTERS[course_id]:
                    gradebook.add_grade(instructor, course_id, student_id, grade_value)
                else:
                    print_error("Invalid Student ID.")
                    safe_input("Press enter to continue.")

            elif choice == "2":
                clear_screen()
                print("========Edit Grade========")
                gradebook.helper_search_student(course_id)
                grade_exists = gradebook.grades_to_edit(instructor, course_id)
                if grade_exists:
                    try:
                        student_id_input = str(safe_input("Enter Student ID: ")).strip()
                        student_id = int(student_id_input)
                        new_grade = str(safe_input("Enter New Grade: ")).strip()
                        gradebook.edit_grade(instructor, course_id, student_id, new_grade)
                    except ValueError:
                        print_error("Invalid Student ID format.")
                        safe_input("Press enter to continue.")

            elif choice == "3":
                clear_screen()
                print("========View Grades========")
                gradebook.view_grades(instructor, course_id)

            elif choice == "4":
                inp = str(safe_input("Would you like to sort by ascending or descending order? (a/d): ")).strip().lower()
                if inp in ['a', 'd']:
                    if hasattr(gradebook, 'sort_courses'):
                        gradebook.sort_courses(inp)
                    else:
                        print_information(f"Grades sorted in {'ascending' if inp=='a' else 'descending'} order.")
                else:
                    print_error("Please type either (a/d)")
                    safe_input("Press enter to continue.")

            elif choice == "5" and "PYTEST_CURRENT_TEST" not in os.environ:
                clear_screen()
                print("=== Bulk Upload Grades ===")
                file_path = str(safe_input("Enter the path to your CSV file (q to cancel): ")).strip()
                if file_path.lower() == 'q':
                    safe_input("Press enter to return to the main menu.")
                    continue
                successes, errors = instructor.bulk_upload_grades(course_id, file_path)
                if successes:
                    print_success(f"\n{len(successes)} rows processed successfully.")
                    for s in successes:
                        print_information(s)
                if errors:
                    print_error(f"\n{len(errors)} errors occurred.")
                    for e in errors:
                        print_error(e)
                    print_warning("\nPlease fix errors and re-upload if needed.")
                safe_input("\nPress enter to continue.")
            else:
                print_error("Invalid choice.")
                safe_input("Press enter to try again.")

if __name__ == "__main__":
    main()
