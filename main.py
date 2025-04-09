from gradebook import Gradebook
from instructor import Instructor
from data import ROSTERS, COURSES, STUDENTS
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

        instructor_id = int(user_input)
        instructor = Instructor(instructor_id)

        if not instructor.is_authenticated():
            print_error("Invalid Instructor ID. Try again. (q for quit)")
            continue

        
        while True:
            clear_screen()
            instructor.display_courses()
            course_id = input("Enter Course ID (q for quit): ")
            if course_id == 'q':
                exit()

            if not instructor.has_access(course_id):
                print_error("Invalid Course ID or Access Denied.")
                continue
            break;
        

        while True:
            clear_screen()
            print(f"\nSelected Course: {course_id}: {COURSES[course_id]["name"]}")
            print("\n1. Add Grade")
            print("2. Edit Grade")
            print("3. View Grades")
            print("4. Logout")

            choice = input("Enter choice: ")

            if choice == "4":
                print_warning("Logging out...")
                input("Press enter to continue.")
                break

            if choice == "1":  # Add Grade
                clear_screen()
                print("========Add Grade========\nStudents in this course:")
                print_information("Students in this course:")
                for sid in ROSTERS[course_id]:

                    print_information(f"- {sid})")

                student_id = int(input("Enter Student ID: "))

                if student_id in ROSTERS[course_id]:
                    grade = input("Enter Grade: ")
                    gradebook.add_grade(instructor, course_id, student_id, grade)

                    print_information(f"- {sid}: {STUDENTS[sid]}")

                #remove the cast to an int, to check if its an empty string
                student_id = input("Enter Student ID: ")
                while(student_id == ""):
                    print("You must enter a student id! ")
                    student_id = input("Enter Student ID: ")

                #cast the string back into an int
                student_id = int (student_id)


                isGradeEmpty = True
                while (isGradeEmpty):
                    grade = input("Enter Grade: ") 

                    if (not grade or grade == "" or grade.startswith(" ")):
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
                student_id = int(input("Enter Student ID: "))
                new_grade = input("Enter New Grade: ")
                gradebook.edit_grade(instructor, course_id, student_id, new_grade)

            elif choice == "3":  # View Grades
                clear_screen()
                print("========View Grades========")
                gradebook.view_grades(instructor, course_id)

            else:
                print_error("Invalid choice.")
                input("Press enter to try again.")


if __name__ == "__main__":
    main()