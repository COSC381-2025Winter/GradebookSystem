from gradebook import Gradebook
from instructor import Instructor
from util import clear_screen
from color_ui import print_error

def main():
    gradebook = Gradebook()

    # Instructor login loop
    while True:
        clear_screen()
        print("\n--- Gradebook System ---")
        user_input = str(input("Enter your Instructor ID (q for quit): "))
        if user_input.lower() == 'q':
            clear_screen()
            exit()
        if not user_input.isnumeric():
            print_error("Invalid Instructor ID. Try again. (q for quit)")
            continue

        instructor = Instructor(int(user_input))
        if not instructor.is_authenticated():
            print_error("Invalid Instructor ID. Try again. (q for quit)")
            continue

        # Theme selection
        theme = str(input("Choose theme (light/dark): ")).lower()
        instructor.set_theme(theme)

        # Course selection
        while True:
            clear_screen()
            instructor.display_courses()
            course_input = str(input("Enter Course ID (q for quit): "))
            if course_input.lower() == 'q':
                clear_screen()
                exit()
            course_id = course_input.upper()
            if not instructor.has_access(course_id):
                print_error("Invalid Course ID or Access Denied.")
                continue
            break

        # Course menu
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
                sid = input("Enter Student ID: ").strip()
                grade_str = input("Enter grade: ").strip()
                if not grade_str:
                    print_error("\tGrade cannot be empty")
                    input("Press enter to continue.")
                    continue
                if not grade_str.replace('.','',1).isdigit():
                    print_error("\tGrade must be numeric")
                    input("Press enter to continue.")
                    continue
                grade = float(grade_str)
                gradebook.add_grade(instructor, course_id, int(sid), grade)

            elif choice == '2':
                clear_screen()
                if not gradebook.grades_to_edit(instructor, course_id):
                    continue
                gradebook.helper_search_student(course_id)
                sid = input("Enter Student ID to edit: ").strip()
                new_grade_str = input("Enter new grade: ").strip()
                if not new_grade_str.replace('.','',1).isdigit():
                    print_error("\tGrade must be numeric")
                    input("Press enter to continue.")
                    continue
                new_grade = float(new_grade_str)
                gradebook.edit_grade(instructor, course_id, int(sid), new_grade)

            elif choice == '3':
                clear_screen()
                gradebook.view_grades(instructor, course_id)

            elif choice == '4':
                clear_screen()
                order = input("Sort ascending or descending? (a/d): ").strip().lower()
                gradebook.sort_courses(order)

            elif choice == '5':
                clear_screen()
                gradebook.add_student(instructor, course_id)

            else:
                print_error("Invalid choice.")
                input("Press enter to continue.")

        # back to login prompt

if __name__ == "__main__":
    main()
