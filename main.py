from gradebook import Gradebook
from instructor import Instructor
from data import ROSTERS, COURSES, STUDENTS
from color_ui import print_success, print_error, print_information, print_warning
from color_theme import apply_theme, list_available_themes
from util import clear_screen
from credentials import PASSWORDS
import getpass

def prompt_for_theme(instructor):
    theme = None
    while theme not in list_available_themes():
        print_information("Available themes: " + ", ".join(list_available_themes()))
        theme = input("Choose a theme (light/dark): ").strip().lower()
        if theme not in list_available_themes():
            print_error("Invalid theme. Please choose 'light' or 'dark'.\n")
    apply_theme(theme)
    print_success(f"Theme '{theme}' applied successfully!\n")

def main():
    gradebook = Gradebook()
    while True:
        clear_screen()
        print("\n--- Gradebook System ---")
        user_input = input("Enter your Instructor ID (q for quit): ")
        if user_input == 'q' or user_input == 'Q':
            clear_screen()
            exit()
        elif not str(user_input).isnumeric():
            print_error("Invalid Instructor ID. Try again. (q for quit)")
            continue

        try:
            instructor_id = int(user_input)
        except ValueError:
            print_error("Error: Instructor not found")
            continue

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

        # 🔹 Prompt for theme after successful login
        prompt_for_theme(instructor)

        while True:
            instructor.display_courses()
            course_id = input("Enter Course ID or Course Name (q for quit / exit to logout): ")
            if course_id.lower() == 'q':
                clear_screen()
                exit()
                
            if course_id.lower() ==  'exit':
                 print_warning("Logging out...")
                 input("Press enter to continue.")
                 main()
            if course_id.replace(' ','').isalpha():        
                course_id = instructor.get_course_code_by_name(course_id)  

            course_id = course_id.upper()

            if not instructor.has_access(course_id):
                print_error("Invalid Course ID or Access Denied.")
                continue
            break;

        while True:
            clear_screen()
            print(f"\nSelected Course: {course_id}: {COURSES[course_id]['name']}")
            print("\n1. Add Grade")
            print("2. Edit Grade")
            print("3. View Grades")
            print("4. Sort Grades")
            print("x. Logout")

            choice = input("Enter choice: ")

            if choice == "x":
                print_warning("Logging out...")
                input("Press enter to continue.")
                break

            if choice == "1":  # Add Grade
                clear_screen()
                print("========Add Grade========\nStudents in this course:")
                print_information("Students in this course:")
                for sid in ROSTERS[course_id]:
                    print_information(f"- {sid}: {STUDENTS[sid]}")


                # call helper method for search_student function
                gradebook.helper_search_student(course_id)

                # replace add grade header
                clear_screen()
                print("========Add Grade========")

                #remove the cast to an int, to check if its an empty string

                student_id = input("Enter Student ID: ")
                while student_id == "":
                    print("You must enter a student id! ")
                    student_id = input("Enter Student ID: ")

                student_id = int(student_id)

                isGradeEmpty = True
                while isGradeEmpty:
                    grade = input("Enter Grade: ") 
                    if not grade or grade == "" or grade.startswith(" "):
                        print("\tGrade cannot be empty")
                        continue
                    else: 
                        isGradeEmpty = False

                try:
                    grade_value = float(grade)
                    if grade_value < 0:
                        print_error("Grade cannot be negative.")
                        input("Press enter to continue.")
                        continue  # Go back to menu
                except ValueError:
                    print_error("Invalid grade format. Please enter a number.")
                    input("Press enter to continue.")
                    continue  # Go back to menu

                if student_id in ROSTERS[course_id]:
                    gradebook.add_grade(instructor, course_id, student_id, grade_value)
                else:
                    print_error("Invalid Student ID.")
                    input("Press enter to continue.")

            elif choice == "2":  # Edit Grade
                clear_screen()
                print("========Edit Grade========")
                # call helper method for search_student function
                gradebook.helper_search_student(course_id)
                grade_exists = gradebook.grades_to_edit(instructor, course_id)

                if(grade_exists == True):
                    student_id = int(input("Enter Student ID: "))
                    new_grade = input("Enter New Grade: ")
                    gradebook.edit_grade(instructor, course_id, student_id, new_grade)

            elif choice == "3":  # View Grades
                clear_screen()
                print("========View Grades========")
                gradebook.view_grades(instructor, course_id)
            
            elif choice == "4":
                try:
                    inp = input("Would you like to sort by ascending or decending order? (a/d): ")
                    inp = inp.lower()
                    if inp == 'a' or inp == 'd':
                        gradebook.sort_courses(inp)
                    else:
                        print("Please type either (a/d)")
                        input("Press enter to continue.")
                except: 
                    print("Please type either (a/d)")
                    input("Press enter to continue.")

            else:
                print_error("Invalid choice.")
                input("Press enter to try again.")

if __name__ == "__main__":
    main()