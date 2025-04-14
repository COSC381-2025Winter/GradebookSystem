from util import clear_screen
from data import COURSES, STUDENTS, ROSTERS
from gradebook import Gradebook
from instructor import Instructor

# Main function to start the Gradebook System
# Handles instructor authentication, theme, course selection, and menu navigation

def main():
    gradebook = Gradebook()

    # Instructor login loop
    while True:
        clear_screen()
        print("\n--- Gradebook System ---")
        user_input = input("Enter your Instructor ID (q for quit): ")
        user_input = str(user_input)
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

        # Theme selection
        theme = input("Choose theme (light/dark): ")
        instructor.set_theme(str(theme).lower())

        # Course selection loop
        while True:
            clear_screen()
            instructor.display_courses()
            course_input = input("Enter Course ID (q for quit): ")
            course_input = str(course_input)
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
            print("\n1. add grade")
            print("2. edit grade")
            print("3. view grades")
            print("4. sort grades")
            print("5. add student")
            print("x. logout")

            choice = input("Enter choice: ")
            choice = str(choice)
            
            if choice == 'x':
                break

            elif choice == '1':
                clear_screen()
                # Optional search before listing
                gradebook.helper_search_student(course_id)
                print("Students in this course:")
                for sid in ROSTERS[course_id]:
                    print(f"- {STUDENTS.get(sid, 'Unknown')} (ID: {sid})")
                sid_input = input("Enter Student ID: ")
                try:
                    student_id = int(sid_input)
                except ValueError:
                    print("\033[91mInvalid student ID.\033[0m")
                    continue

                while True:
                    grade = input("Enter Grade: ")
                    if not grade.strip():
                        print("\tGrade cannot be empty")
                        continue
                    try:
                        numeric = float(grade)
                        if numeric < 0:
                            print("\033[91mGrade cannot be negative.\033[0m")
                            break
                    except ValueError:
                        print("\033[91mInvalid grade format. Please enter a number.\033[0m")
                        break
                    gradebook.add_grade(instructor, course_id, student_id, numeric)
                    break

            elif choice == '2':
                clear_screen()
                try:
                    sid = int(input("Enter Student ID: "))
                    new_grade = float(input("Enter New Grade: "))
                except ValueError:
                    print("\033[91mInvalid input.\033[0m")
                    continue
                gradebook.edit_grade(instructor, course_id, sid, new_grade)

            elif choice == '3':
                clear_screen()
                gradebook.view_grades(instructor, course_id)

            elif choice == '4':
                clear_screen()
                order = input("Would you like to sort by ascending or descending order? (a/d): ")
                order = order.lower()
                if order in ['a', 'd']:
                    gradebook.sort_courses(order)
                else:
                    print("Please type either (a/d)")

            elif choice == '5':
                clear_screen()
                print("========Add Student========")
                try:
                    new_student_id = int(input("Enter New Student ID: "))
                    grade_input = input("Enter Grade (press enter to default to 0): ")
                    default_grade = int(grade_input) if grade_input.strip() != "" else 0
                    if new_student_id not in ROSTERS[course_id]:
                        ROSTERS[course_id].append(new_student_id)
                        gradebook.add_grade(instructor, course_id, new_student_id, default_grade, force=True)
                        print(f"\033[92mStudent {new_student_id} added with grade {default_grade}.\033[0m")
                    else:
                        print(f"\033[93mStudent {new_student_id} is already in the course.\033[0m")
                except ValueError:
                    print("\033[91mInvalid input. Please enter valid numbers.\033[0m")
                input("Press enter to continue.")

            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()
