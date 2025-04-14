from util import clear_screen
from data import INSTRUCTORS, COURSES, STUDENTS, ROSTERS
from gradebook import Gradebook
from instructor import Instructor


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
            print("\033[91mInvalid Instructor ID. Try again. (q for quit)\033[0m")
            continue

        instructor = Instructor(int(user_input))
        if not instructor.is_authenticated():
            print("\033[91mInvalid Instructor ID. Try again. (q for quit)\033[0m")
            continue

        # Theme selection (apply only if supported)
        theme = input("Choose theme (light/dark): ").strip().lower()
        if hasattr(instructor, 'set_theme'):
            try:
                instructor.set_theme(theme)
            except ValueError:
                pass

        # Course selection loop
        while True:
            clear_screen()
            instructor.display_courses()
            course_input = str(input("Enter Course ID (q for quit): "))
            if course_input.lower() == 'q':
                clear_screen()
                exit()
            course_id = course_input.upper()
            if not instructor.has_access(course_id):
                print("\033[91mInvalid Course ID or Access Denied.\033[0m")
                continue
            break

        # Course menu loop
        while True:
            clear_screen()
            print("1. add grade")
            print("2. edit grade")
            print("3. view grades")
            print("4. sort grades")
            # only show add student in dark theme
            if theme == 'dark':
                print("5. add student")
            print("x. logout")

            choice = str(input("Enter choice: "))
            if choice == 'x':
                break

            # Add Grade
            if choice == '1':
                clear_screen()
                # Optional search
                if hasattr(gradebook, 'helper_search_student'):
                    gradebook.helper_search_student(course_id)
                # List students
                for sid in ROSTERS.get(course_id, []):
                    print(f"- {sid}: {STUDENTS.get(sid, 'Unknown')}")
                try:
                    student_id = int(input("Enter Student ID: "))
                except ValueError:
                    print("\033[91mInvalid student ID.\033[0m")
                    input("Press enter to continue.")
                    continue
                grade_input = input("Enter Grade: ")
                if not grade_input.strip():
                    print("\tGrade cannot be empty")
                    input("Press enter to continue.")
                    continue
                try:
                    grade = float(grade_input)
                    if grade < 0:
                        print("\033[91mGrade cannot be negative.\033[0m")
                        input("Press enter to continue.")
                        continue
                except ValueError:
                    print("\033[91mInvalid grade format. Please enter a number.\033[0m")
                    input("Press enter to continue.")
                    continue
                gradebook.add_grade(instructor, course_id, student_id, grade)

            # Edit Grade
            elif choice == '2':
                clear_screen()
                if hasattr(gradebook, 'helper_search_student'):
                    gradebook.helper_search_student(course_id)
                try:
                    student_id = int(input("Enter Student ID: "))
                    new_grade_input = input("Enter New Grade: ")
                    new_grade = float(new_grade_input)
                except ValueError:
                    print("\033[91mInvalid input.\033[0m")
                    input("Press enter to continue.")
                    continue
                gradebook.edit_grade(instructor, course_id, student_id, new_grade)

            # View Grades
            elif choice == '3':
                clear_screen()
                grades = gradebook.view_grades(instructor, course_id)
                if isinstance(grades, dict):
                    for sid, data in grades.items():
                        name = STUDENTS.get(sid, f"Student {sid}")
                        print(f"{name} ({sid}): {data['grade']}")
                else:
                    print(grades)
                input("Press enter to continue.")

            # Sort Grades
            elif choice == '4':
                clear_screen()
                order = input("Sort by ascending or descending? (a/d): ").lower()
                result = gradebook.sort_courses(order)
                if isinstance(result, str):
                    print(result)
                input("Press enter to continue.")

            # Add Student
            elif choice == '5' and theme == 'dark':
                clear_screen()
                print("========Add Student========")
                try:
                    new_student_id = int(input("Enter New Student ID: "))
                    grade_input = input("Enter Grade (press enter to default to 0): ")
                    default_grade = float(grade_input) if grade_input.strip() else 0.0
                except ValueError:
                    print("\033[91mInvalid input. Please enter valid numbers.\033[0m")
                    input("Press enter to continue.")
                    continue
                if new_student_id not in ROSTERS.get(course_id, []):
                    ROSTERS.setdefault(course_id, []).append(new_student_id)
                    gradebook.add_grade(instructor, course_id, new_student_id, default_grade, force=True)
                    print(f"\033[92mStudent {new_student_id} added with grade {default_grade}.\033[0m")
                else:
                    print(f"\033[93mStudent {new_student_id} is already in the course.\033[0m")
                input("Press enter to continue.")

            else:
                print("Please type either (1/2/3/4/x)" + (" or 5" if theme == 'dark' else ""))
                input("Press enter to continue.")


if __name__ == "__main__":
    main()

