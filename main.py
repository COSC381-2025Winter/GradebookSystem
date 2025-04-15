from gradebook import Gradebook
from instructor import Instructor
from data import ROSTERS, COURSES, STUDENTS
from color_ui import print_success, print_error, print_information, print_warning
from color_theme import apply_theme, list_available_themes
from util import clear_screen
from credentials import PASSWORDS
import getpass

def prompt_for_theme(instructor):
    """Prompt user to select a color theme"""
    theme = None
    while theme not in list_available_themes():
        print_information("Available themes: " + ", ".join(list_available_themes()))
        theme = input("Choose a theme (light/dark): ").strip().lower()
        if theme not in list_available_themes():
            print_error("Invalid theme. Please choose 'light' or 'dark'.\n")
    apply_theme(theme)
    instructor.set_theme(theme)
    print_success(f"Theme '{theme}' applied successfully!\n")

def main():
    gradebook = Gradebook()
    while True:
        clear_screen()
        print("\n--- Gradebook System ---")
        user_input = input("Enter your Instructor ID (q for quit): ")
        
        # Handle quit command
        if user_input.lower() == 'q':
            clear_screen()
            exit()

        # Validate instructor ID
        if not str(user_input).isnumeric():
            print_error("Invalid Instructor ID. Try again. (q for quit)")
            continue

        try:
            instructor_id = int(user_input)
        except ValueError:
            print_error("Error: Instructor not found")
            continue

        # Authentication
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

        # Set theme after successful login
        prompt_for_theme(instructor)

        # Course selection loop
        while True:
            clear_screen()
            instructor.display_courses()
            course_id = input("Enter Course ID (q for quit / exit to logout): ").strip().lower()
            
            if course_id == 'q':
                clear_screen()
                exit()
                
            if course_id == 'exit':
                print_warning("Logging out...")
                input("Press enter to continue.")
                break

            course_id = course_id.upper()
            if not instructor.has_access(course_id):
                print_error("Invalid Course ID or Access Denied.")
                continue
            break

        # Skip to login if user chose to logout
        if course_id.lower() == 'exit':
            continue

        # Main menu loop
        while True:
            clear_screen()
            print(f"\nSelected Course: {course_id}: {COURSES[course_id]['name']}")
            print("\n1. Add Grade")
            print("2. Edit Grade")
            print("3. View Grades")
            print("4. Sort Grades")
            print("5. Bulk Upload Grades")
            print("x. Logout")

            choice = input("Enter choice: ").strip().lower()

            # Logout option
            if choice == "x":
                print_warning("Logging out...")
                input("Press enter to continue.")
                break

            # Add Grade
            elif choice == "1":
                clear_screen()
                print("========Add Grade========")
                print("Students in this course:")
                for sid in ROSTERS[course_id]:
                    print_information(f"- {sid}: {STUDENTS[sid]}")

                # Student search helper
                gradebook.helper_search_student(course_id)
                clear_screen()
                print("========Add Grade========")

                # Get student ID
                student_id = input("Enter Student ID: ").strip()
                while not student_id:
                    print("You must enter a student ID!")
                    student_id = input("Enter Student ID: ").strip()

                try:
                    student_id = int(student_id)
                except ValueError:
                    print_error("Invalid Student ID format.")
                    input("Press enter to continue.")
                    continue

                # Get grade
                grade = ""
                while not grade.strip():
                    grade = input("Enter Grade: ").strip()
                    if not grade:
                        print("\tGrade cannot be empty")

                try:
                    grade_value = float(grade)
                    if grade_value < 0:
                        print_error("Grade cannot be negative.")
                        input("Press enter to continue.")
                        continue
                except ValueError:
                    print_error("Invalid grade format. Please enter a number.")
                    input("Press enter to continue.")
                    continue

                if student_id in ROSTERS[course_id]:
                    gradebook.add_grade(instructor, course_id, student_id, grade_value)
                else:
                    print_error("Invalid Student ID.")
                    input("Press enter to continue.")

            # Edit Grade
            elif choice == "2":
                clear_screen()
                print("========Edit Grade========")
                gradebook.helper_search_student(course_id)
                grade_exists = gradebook.grades_to_edit(instructor, course_id)

                if grade_exists:
                    try:
                        student_id = int(input("Enter Student ID: "))
                        new_grade = input("Enter New Grade: ").strip()
                        gradebook.edit_grade(instructor, course_id, student_id, new_grade)
                    except ValueError:
                        print_error("Invalid Student ID format.")
                        input("Press enter to continue.")

            # View Grades
            elif choice == "3":
                clear_screen()
                print("========View Grades========")
                gradebook.view_grades(instructor, course_id)

            # Sort Grades
            elif choice == "4":
                inp = input("Would you like to sort by ascending or descending order? (a/d): ").lower()
                if inp in ['a', 'd']:
                    gradebook.sort_courses(inp)
                else:
                    print("Please type either (a/d)")
                    input("Press enter to continue.")

            # Bulk Upload
            elif choice == "5":
                clear_screen()
                print("=== Bulk Upload Grades ===")

                file_path = input("Enter the path to your CSV file (q to cancel): ").strip()
                if file_path.lower() == 'q':
                    input("Press enter to return to the main menu.")
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

                input("\nPress enter to continue.")

            # Invalid choice
            else:
                print_error("Invalid choice.")
                input("Press enter to try again.")

if __name__ == "__main__":
    main()