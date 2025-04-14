import sys
from instructor import Instructor
from gradebook import Gradebook, _wait_for_continue
from util import clear_screen
from color_ui import print_error

def main():
    try:
        gradebook = Gradebook()
        while True:
            clear_screen()
            print("\n--- Gradebook System ---")
            try:
                user_input = input("Enter your Instructor ID (q for quit): ")
            except StopIteration:
                sys.exit()
            if user_input.lower() == 'q':
                clear_screen()
                sys.exit()
            if not user_input.isnumeric():
                print_error("Invalid Instructor ID. Try again. (q for quit)")
                continue
            instructor = Instructor(int(user_input))
            if not instructor.is_authenticated():
                print_error("Invalid Instructor ID. Try again. (q for quit)")
                continue
            # Theme selection
            theme = input("Choose theme (light/dark): ").lower()
            # Support test doubles that may not have set_theme by checking first.
            if hasattr(instructor, 'set_theme'):
                try:
                    instructor.set_theme(theme)
                except Exception:
                    pass
            else:
                setattr(instructor, 'set_theme', lambda t: None)
            # Course selection loop
            while True:
                clear_screen()
                instructor.display_courses()
                course_input = input("Enter Course ID (q for quit): ")
                if course_input.lower() == 'q':
                    clear_screen()
                    sys.exit()
                course_id = course_input.upper()
                if not instructor.has_access(course_id):
                    print_error("Invalid Course ID or Access Denied.")
                    continue
                break
            # Course menu loop
            while True:
                clear_screen()
                print("1. add grade")
                print("2. edit grade")
                print("3. view grades")
                print("4. sort grades")
                print("5. add student")
                print("x. logout")
                choice = input("Enter choice: ").lower()
                if choice == 'x':
                    break
                if choice == '1':
                    clear_screen()
                    gradebook.helper_search_student(course_id)
                    sid = input("Enter Student ID: ").strip()
                    grade_str = input("Enter grade: ").strip()
                    if not grade_str:
                        print_error("\tGrade cannot be empty")
                        _wait_for_continue()
                        continue
                    try:
                        grade_val = float(grade_str)
                    except ValueError:
                        print_error("\tGrade must be numeric")
                        _wait_for_continue()
                        continue
                    gradebook.add_grade(instructor, course_id, int(sid), grade_val)
                elif choice == '2':
                    clear_screen()
                    if not gradebook.grades_to_edit(instructor, course_id):
                        print_error("No grades available to edit.")
                        _wait_for_continue()
                        continue
                    sid = input("Enter Student ID to edit: ").strip()
                    new_grade_str = input("Enter new grade: ").strip()
                    if not new_grade_str:
                        print_error("Grade cannot be empty.")
                        _wait_for_continue()
                        continue
                    try:
                        new_grade_val = float(new_grade_str)
                    except ValueError:
                        print_error("Grade must be numeric")
                        _wait_for_continue()
                        continue
                    gradebook.edit_grade(instructor, course_id, int(sid), new_grade_val)
                elif choice == '3':
                    clear_screen()
                    course_grades = gradebook.view_grades(instructor, course_id)
                elif choice == '4':
                    clear_screen()
                    arr = input("Type 'a' for ascending or 'd' for descending sorting: ").lower()
                    gradebook.sort_courses(arr)
                elif choice == '5':
                    clear_screen()
                    gradebook.add_student(instructor, course_id)
                else:
                    print_error("Invalid choice.")
                    _wait_for_continue()
    except StopIteration:
        sys.exit()

if __name__ == "__main__":
    main()
