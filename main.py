rom util import clear_screen
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

        if str(user_input).lower() == 'q':
            clear_screen()
            exit()
        elif not str(user_input).isnumeric():
            print("\033[91mInvalid Instructor ID. Try again. (q for quit)\033[0m")
            continue

        try:
            instructor_id = int(user_input)
        except ValueError:
            print("\033[91mPlease enter a valid number.\033[0m")
            input("Press enter to continue.")
            continue

        instructor = Instructor(instructor_id)

        if not instructor.is_authenticated():
            print("\033[91mInvalid Instructor ID. Try again. (q for quit)\033[0m")
            input("Press enter to continue.")
            continue

        # Instructor authenticated, prompt for course selection
        while True:
            clear_screen()
            instructor.display_courses()
            course_id_input = input("Enter Course ID (q for quit): ")

            if str(course_id_input).lower() == 'q':
                clear_screen()
                exit()

            try:
                course_id = str(course_id_input).upper()
            except AttributeError:
                print("\033[91mInvalid Course ID format.\033[0m")
                input("Press enter to continue.")
                continue

            if not instructor.has_access(course_id):
                print("\033[91mInvalid Course ID or Access Denied.\033[0m")
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
                print("\033[93mLogging out...\033[0m")
                input("Press enter to continue.")
                break

            elif choice == "1":
                clear_screen()
                print("========Add Grade========\nStudents in this course:")
                print("\033[94mStudents in this course:\033[0m")
                for sid in ROSTERS[course_id]:
                    print(f"\033[94m- {sid}: {STUDENTS.get(sid, 'Unknown')}\033[0m")

                try:
                    student_id = int(input("Enter Student ID: "))
                except ValueError:
                    print("\033[91mInvalid student ID.\033[0m")
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
                        print("\033[91mGrade cannot be negative.\033[0m")
                        continue
                except ValueError:
                    print("\033[91mInvalid grade format. Please enter a number.\033[0m")
                    continue

                gradebook.add_grade(instructor, course_id, student_id, numeric_grade)

            elif choice == "2":
                clear_screen()
                try:
                    student_id = int(input("Enter Student ID: "))
                    new_grade = float(input("Enter New Grade: "))
                    gradebook.edit_grade(instructor, course_id, student_id, new_grade)
                except ValueError:
                    print("\033[91mInvalid input.\033[0m")
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
                        print("\033[92mStudent {} added with grade {}.\033[0m".format(new_student_id, default_grade))
                    else:
                        print("\033[93mStudent {} is already in the course.\033[0m".format(new_student_id))
                except ValueError:
                    print("\033[91mInvalid input. Please enter valid numbers.\033[0m")
                input("Press enter to continue.")

if __name__ == "__main__":
    main()
