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
            # Convert input to string to avoid issues when tests supply ints.
            user_input = str(input("Enter your Instructor ID (q for quit): "))
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
            theme = str(input("Choose theme (light/dark): ")).lower()
            try:
                instructor.set_theme(theme)
            except Exception as e:
                print_error(str(e))
            # Course selection loop
            while True:
                clear_screen()
                instructor.display_courses()
                course_input = str(input("Enter Course ID (q for quit): "))
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
                choice = str(input("Enter choice: ")).lower()
                if choice == 'x':
                    break
                if choice == '1':
                    clear_screen()
                    gradebook.helper_search_student(course_id)
                    sid = str(input("Enter Student ID: ")).strip()
                    # Loop until a valid grade is entered.
                    while True:
                        grade_str = str(input("Enter grade: ")).strip()
                        if not grade_str:
                            print_error("\tGrade cannot be empty")
                            _wait_for_continue()
                            continue
                        try:
                            grade_val = float(grade_str)
                        except ValueError:
                            print_error("\tInvalid grade format")
                            _wait_for_continue()
                            continue
                        if grade_val < 0:
                            print_error("Grade cannot be negative")
                            _wait_for_continue()
                            continue
                        break
                    gradebook.add_grade(instructor, course_id, int(sid), grade_val)
                elif choice == '2':
                    clear_screen()
                    editable = gradebook.grades_to_edit(instructor, course_id)
                    if not editable:
                        print_error("No grades available to edit.")
                        _wait_for_continue()
                        continue
                    sid = str(input("Enter Student ID to edit: ")).strip()
                    # Loop for valid new grade.
                    while True:
                        new_grade_str = str(input("Enter new grade: ")).strip()
                        if not new_grade_str:
                            print_error("Grade cannot be empty.")
                            _wait_for_continue()
                            continue
                        try:
                            new_grade_val = float(new_grade_str)
                        except ValueError:
                            print_error("\tInvalid grade format")
                            _wait_for_continue()
                            continue
                        if new_grade_val < 0:
                            print_error("Grade cannot be negative")
                            _wait_for_continue()
                            continue
                        break
                    gradebook.edit_grade(instructor, course_id, int(sid), new_grade_val)
                elif choice == '3':
                    clear_screen()
                    _ = gradebook.view_grades(instructor, course_id)
                elif choice == '4':
                    clear_screen()
                    arr = str(input("Type 'a' for ascending or 'd' for descending sorting: ")).lower()
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
