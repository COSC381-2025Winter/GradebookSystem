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
            course_id = course_id.upper()
            if not instructor.has_access(course_id):
                print_error("Invalid Course ID or Access Denied.")
                continue
            break

        while True:
            clear_screen()
            print(f"\nSelected Course: {course_id}: {COURSES[course_id]['name']}")
            print("\n1. Add Grade")
            print("2. Edit Grade")
            print("3. View Grades")
            print("4. Sort Grades")
            print("5. Bulk Upload Grades")
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
                    print_information(f"- {sid}: {STUDENTS[sid]}")

                student_id = input("Enter Student ID: ")
                while student_id == "":
                    print("You must enter a student ID!")
                    student_id = input("Enter Student ID: ")

                student_id = int(student_id)

                isGradeEmpty = True
                while isGradeEmpty:
                    grade = input("Enter Grade: ") 
                    if not grade or grade.startswith(" "):
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

                if student_id in ROSTERS[course_id]:
                    gradebook.add_grade(instructor, course_id, student_id, grade_value)
                else:
                    print_error("Invalid Student ID.")
                    input("Press enter to continue.")

            elif choice == "2":
                clear_screen()
                print("========Edit Grade========")
                student_id = int(input("Enter Student ID: "))
                new_grade = input("Enter New Grade: ")
                gradebook.edit_grade(instructor, course_id, student_id, new_grade)

            elif choice == "3":
                clear_screen()
                print("========View Grades========")
                gradebook.view_grades(instructor, course_id)

            elif choice == "4":
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
                print("=== Bulk Upload Grades ===")

                file_path = input("Enter the path to your CSV file (q to cancel): ")
                if file_path.lower() == 'q':
                    input("Press enter to return to the main menu.")
                    continue

                successes, errors = instructor.bulk_upload_grades(course_id, file_path)

                if successes:
                    print_success(f"\n{len(successes)} rows processed successfully.")
                    for s in successes:
                        print_information(s)

                if errors:
                    print_error(f"\n{len(errors)} errors occurred.")
                    for e in errors:
                        print_error(e)
                    print_warning("\nPlease fix errors and re-upload if needed.")

                input("\nPress enter to continue.")

            else:
                print_error("Invalid choice.")
                input("Press enter to try again.")

if __name__ == "__main__":
    main()
