import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


from gradebook import Gradebook
from instructor import Instructor
from data import ROSTERS, COURSES, STUDENTS
from color_ui import print_success, print_error, print_information, print_warning
from color_theme import apply_theme, list_available_themes
from util import clear_screen
import time
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
        
        clear_screen()
        user_input = input("Enter your Instructor ID  (q for quit) 0 for new instructor: ")
        if user_input == 'q' or user_input == 'Q':
            clear_screen()
            print_warning("--- Gradebook System ---\nEnding program...") 
            exit()
        elif user_input == '0':
            clear_screen()
            instructor_name = input("What is the Instructor's name (e.g., Dr. Smith): ").strip()
            if not instructor_name:
                print_error("Instructor name cannot be empty")
                continue

            password = getpass.getpass("Enter a password for the instructor: ").strip()
            if not password:
                print_error("Password cannot be empty")
                continue

            instructor_id = Instructor.add_instructor(instructor_name, password)
            print_success(f"Instructor '{instructor_name}' registered with ID {instructor_id}")
            input("Press Enter to continue...")

                

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

        prompt_for_theme(instructor)

        loggout = False
        while not loggout:  # Stay logged in
            
            # Course selection loop
            while True and not loggout:
                clear_screen()
                print_success("Instructor found!\n") 
                instructor.display_courses()
                course_id = input("Enter Course ID or Course Name (l or exit to logout): ")
    
                if course_id.lower() ==  'exit' or course_id.lower() == 'l':
                    print_warning("Logging out...")
                    loggout = True
                    input("Press enter to continue.")

                if course_id.replace(' ','').isalpha():        
                    course_id = instructor.get_course_code_by_name(course_id)  

                course_id = course_id.upper()
                if not instructor.has_access(course_id):
                    print_error("Invalid Course ID or Access Denied.")
                    continue

                print_success("Valid Course ID!")
                time.sleep(1.5)
                break  # Valid course selected

            # Course menu
            while True and not loggout:
                clear_screen()
                print(f"\nSelected Course: {course_id}: {COURSES[course_id]['name']}")
                print("\n1. Add Grade")
                print("2. Edit Grade")
                print("3. View Grades")
                print("4. Sort Grades")
                print("x. Switch Course")

                choice = input("Enter choice: ")

                if choice == "x":
                    print_information("Switching course...")
                    input("Press enter to continue.")
                    break  # Go back to course selection

                elif choice == "1":  # Add Grade
                    clear_screen()
                    print("========Add Grade========\nStudents in this course:")
                    print_information("Students in this course:")
                    for sid in ROSTERS[course_id]:
                        print_information(f"- {sid}: {STUDENTS[sid]}")

                    gradebook.helper_search_student(course_id)

                    clear_screen()
                    print("========Add Grade========")

                    student_id = input("Enter Student ID: ")
                    while student_id == "":
                        print("You must enter a student id! ")
                        student_id = input("Enter Student ID: ")

                    student_id = int(student_id)

                    if student_id in ROSTERS[course_id]:
                        print_success(f"Student found!\n")

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
                                continue
                        except ValueError:
                            print_error("Invalid grade format. Please enter a number.")
                            input("Press enter to continue.")
                            continue

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
                            time.sleep(1.5)
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
