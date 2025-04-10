from gradebook import Gradebook
from instructor import Instructor
from data import ROSTERS, COURSES
from color_ui import print_success, print_error, print_information, print_warning
from util import clear_screen

def main():
    gradebook = Gradebook()
    while True:
        clear_screen()
        print("\n--- Gradebook System ---")
        user_input = input("Enter your Instructor ID (q for quit): ")
        if user_input == 'q':
            clear_screen()
            exit()

        try:
            instructor_id = int(user_input)
        except ValueError:
            print_error("Please enter a valid number.")
            input("Press enter to continue.")
            continue

        instructor = Instructor(instructor_id)

        if not instructor.is_authenticated():
            print_error("Invalid Instructor ID. Try again. (q for quit)")
            input("Press enter to continue.")
            continue

        while True:
            clear_screen()
            instructor.display_courses()
            course_id = input("Enter Course ID (q for quit): ")
            if course_id == 'q':
                exit()

            if not instructor.has_access(course_id):
                print_error("Invalid Course ID or Access Denied.")
                input("Press enter to continue.")
                continue
            break

        while True:
            clear_screen()
            print(f"\nSelected Course: {course_id}: {COURSES[course_id]['name']}")
            print("\n1. Add Grade")
            print("2. Edit Grade")
            print("3. View Grades")
            print("4. Add Student")  # <-- New Option
            print("5. Logout")

            choice = input("Enter choice: ")

            if choice == "5":
                print_warning("Logging out...")
                input("Press enter to continue.")
                break

            elif choice == "1":  # Add Grade
                clear_screen()
                print("========Add Grade========\nStudents in this course:")
                print_information("Students in this course:")
                for sid in ROSTERS[course_id]:
                    print_information(f"- {sid})")

                try:
                    student_id = int(input("Enter Student ID: "))
                    grade = int(input("Enter Grade: "))

                    if student_id in ROSTERS[course_id]:
                        gradebook.add_grade(instructor, course_id, student_id, grade)
                    else:
                        print_error("Invalid Student ID.")
                        input("Press enter to continue.")
                except ValueError:
                    print_error("Invalid input.")
                    input("Press enter to continue.")

            elif choice == "2":  # Edit Grade
                clear_screen()
                print("========Edit Grade========")
                try:
                    student_id = int(input("Enter Student ID: "))
                    new_grade = int(input("Enter New Grade: "))
                    gradebook.edit_grade(instructor, course_id, student_id, new_grade)
                except ValueError:
                    print_error("Invalid input.")
                    input("Press enter to continue.")

            elif choice == "3":  # View Grades
                clear_screen()
                print("========View Grades========")
                gradebook.view_grades(instructor, course_id)

            elif choice == "4":  # Add Student
                clear_screen()
                print("========Add Student========")
                try:
                    new_student_id = int(input("Enter New Student ID: "))
                    grade_input = input("Enter Grade (press enter to default to 0): ")
                    default_grade = int(grade_input) if grade_input.strip() != "" else 0

                    if new_student_id not in ROSTERS[course_id]:
                        ROSTERS[course_id].append(new_student_id)
                        gradebook.add_grade(instructor, course_id, new_student_id, default_grade, force=True)
                        print_success(f"Student {new_student_id} added with grade {default_grade}.")
                    else:
                        print_warning(f"Student {new_student_id} is already in the course.")

                except ValueError:
                    print_error("Invalid input. Please enter valid numbers.")

                input("Press enter to continue.")

            else:
                print_error("Invalid choice.")
                input("Press enter to try again.")

if __name__ == "__main__":
    main()
