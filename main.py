from util import clear_screen, print_error, print_success, print_warning, print_information
from data import INSTRUCTORS, COURSES, STUDENTS, ROSTERS
from gradebook import Gradebook
from instructor import Instructor

# Main function to start the Gradebook System
# Handles instructor authentication and menu navigation
def main():
    gradebook = Gradebook()

    while True:
        clear_screen()
        print("\n--- Gradebook System ---")
        user_input = input("Enter your Instructor ID (q for quit): ")
        user_input = str(user_input)
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
        theme = input("Choose theme (light/dark): ")
        instructor.set_theme(str(theme).lower())

        # Instructor authenticated, prompt for course selection
        while True:
            clear_screen()
            instructor.display_courses()
            course_id = input("Enter Course ID (q for quit / exit to logout): ")
            if course_id.lower() == 'q':
                clear_screen()
                exit()

            if course_id.lower() == 'exit':
                print_warning("Logging out...")
                input("Press enter to continue.")
                main()

            course_id = course_id.upper()
            if not instructor.has_access(course_id):
                print_error("Invalid Course ID or Access Denied.")
                input("Press enter to continue.")
                continue

            break  # Valid course selected

        # Course selected, present options to the instructor
        while True:
            clear_screen()
            print(f"\nSelected Course: {course_id}: {COURSES[course_id]['name']}")
            print("\n1. Add Grade")
            print("2. Edit Grade")
            print("3. View Grades")
            print("4. Sort Grades")
            print("5. Add Student")
            print("x. Logout")

            choice = input("Enter choice: ")

            if choice == "x":
                print_warning("Logging out...")
                input("Press enter to continue.")
                break

            elif choice == "1":
                clear_screen()
                print("========Add Grade========\nStudents in this course:")
                print_information("Students in this course:")
                for sid in ROSTERS[course_id]:
                    print_information(f"- {sid}: {STUDENTS.get(sid, 'Unknown')}")

                try:
                    student_id = int(input("Enter Student ID: "))
                except ValueError:
                    print_error("Invalid student ID.")
                    continue

                isGradeEmpty = True
                while isGradeEmpty:
                    grade = input("Enter Grade: ")
                    if not grade or grade.strip() == "":
                        print("\tGrade cannot be empty")
                        continue
                    else:
                        isGradeEmpty = False

                try:
                    numeric_grade = float(grade)
                    if numeric_grade < 0:
                        print_error("Grade cannot be negative.")
                        continue
                except ValueError:
                    print_error("Invalid grade format. Please enter a number.")
                    continue

                gradebook.add_grade(instructor, course_id, student_id, numeric_grade)

            elif choice == "2":
                clear_screen()
                try:
                    student_id = int(input("Enter Student ID: "))
                    new_grade = float(input("Enter New Grade: "))
                    gradebook.edit_grade(instructor, course_id, student_id, new_grade)
                except ValueError:
                    print_error("Invalid input.")
                    input("Press enter to try again.")
                    continue

            elif choice == "3":
                clear_screen()
                gradebook.view_grades(course_id)
                input("Press enter to continue.")

            elif choice == "4":
                clear_screen()
                try:
                    inp = input("Would you like to sort by ascending or descending order? (a/d): ")
                    inp = inp.lower()
                    if inp in ['a', 'd']:
                        gradebook.sort_courses(inp)
                    else:
                        print("Please type either (a/d)")
                        input("Press enter to continue.")
                except:
                    print("Please type either (a/d)")
                    input("Press enter to continue.")

            elif choice == "5":
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

if __name__ == "__main__":
    main()
