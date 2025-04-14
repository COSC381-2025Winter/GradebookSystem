import sys
from instructor import Instructor
from gradebook import Gradebook, clear_screen
from util import clear_screen as real_clear_screen
from color_ui import print_error

# Local clear_screen that only clears if stdout is a TTY.
def clear_screen_wrapper():
    import sys
    if sys.stdout.isatty():
        real_clear_screen()

def main():
    try:
        gradebook = Gradebook()
        # Log in:
        clear_screen_wrapper()
        print("\n--- Gradebook System ---")
        user_input = str(input("Enter your Instructor ID (q for quit): ")).strip()
        if user_input.lower() == 'q':
            clear_screen_wrapper()
            sys.exit()
        if not user_input.isnumeric():
            print_error("Invalid Instructor ID. Try again. (q for quit)")
            sys.exit()
        instructor = Instructor(int(user_input))
        if not instructor.is_authenticated():
            print_error("Invalid Instructor ID. Try again. (q for quit)")
            sys.exit()
        theme = str(input("Choose theme (light/dark): ")).strip().lower()
        try:
            instructor.set_theme(theme)
        except Exception as e:
            print_error(str(e))
        # Course selection:
        while True:
            clear_screen_wrapper()
            instructor.display_courses()
            course_input = str(input("Enter Course ID (q for quit): ")).strip()
            if course_input.lower() == 'q':
                clear_screen_wrapper()
                sys.exit()
            course_id = str(course_input).upper()
            if not instructor.has_access(course_id):
                print_error("Invalid Course ID or Access Denied.")
                continue
            break
        # Main menu:
        while True:
            clear_screen_wrapper()
            print("1. add grade")
            print("2. edit grade")
            print("3. view grades")
            print("4. sort grades")
            print("5. add student")
            print("x. logout")
            choice = str(input("Enter choice: ")).strip().lower()
            if choice == 'x':
                sys.exit()  # Exit immediately on logout.
            if choice == '1':
                clear_screen_wrapper()
                gradebook.helper_search_student(course_id)
                sid = str(input("Enter Student ID: ")).strip()
                # Loop until a valid grade is entered.
                while True:
                    grade_str = str(input("Enter grade: ")).strip()
                    if grade_str == "":
                        print_error("\tGrade cannot be empty")
                        continue
                    try:
                        grade_val = float(grade_str)
                    except ValueError:
                        print_error("\tInvalid grade format")
                        continue
                    if grade_val < 0:
                        print_error("Grade cannot be negative")
                        continue
                    break
                gradebook.add_grade(instructor, course_id, int(sid), grade_val)
            elif choice == '2':
                clear_screen_wrapper()
                gradebook.helper_search_student(course_id)
                if not gradebook.grades_to_edit(instructor, course_id):
                    print_error("No grades available to edit.")
                    continue
                sid = str(input("Enter Student ID to edit: ")).strip()
                while True:
                    new_grade_str = str(input("Enter new grade: ")).strip()
                    if new_grade_str == "":
                        print_error("Grade cannot be empty.")
                        continue
                    try:
                        new_grade_val = float(new_grade_str)
                    except ValueError:
                        print_error("\tInvalid grade format")
                        continue
                    if new_grade_val < 0:
                        print_error("Grade cannot be negative")
                        continue
                    break
                gradebook.edit_grade(instructor, course_id, int(sid), new_grade_val)
            elif choice == '3':
                clear_screen_wrapper()
                _ = gradebook.view_grades(instructor, course_id)
            elif choice == '4':
                clear_screen_wrapper()
                arr = str(input("Type 'a' for ascending or 'd' for descending sorting: ")).strip().lower()
                gradebook.sort_courses(arr)
            elif choice == '5':
                clear_screen_wrapper()
                gradebook.add_student(instructor, course_id)
            else:
                print_error("Invalid choice.")
    except StopIteration:
        sys.exit()

if __name__ == "__main__":
    main()
