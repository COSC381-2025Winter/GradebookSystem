from gradebook import Gradebook
from instructor import Instructor
from data import ROSTERS, COURSES
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
            print("Invalid Instructor ID. Try again. (q for quit)")
            continue

        
        while True:
            clear_screen()
            instructor.display_courses()
            course_id = input("Enter Course ID (q for quit): ")
            if course_id == 'q':
                exit()

            if not instructor.has_access(course_id):
                print("Invalid Course ID or Access Denied.")
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
                input("Logging out... Press enter to continue.")
                break

            if choice == "1":  # Add Grade
                clear_screen()
                print("========Add Grade========\nStudents in this course:")
                for sid in ROSTERS[course_id]:
                    print(f"- {sid})")

                student_id = int(input("Enter Student ID: "))
                grade = input("Enter Grade: ")

                if student_id in ROSTERS[course_id]:
                    gradebook.add_grade(instructor, course_id, student_id, grade)
                else:
                    input("Invalid Student ID. Press enter to continue.")

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
                input("Invalid choice. Press enter to try again.")


if __name__ == "__main__":
    main()