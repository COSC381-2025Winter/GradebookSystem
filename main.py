from gradebook import Gradebook
from instructor import Instructor
from data import ROSTERS, COURSES
from colorama import Fore, Back, Style

def main():
    gradebook = Gradebook()
    while True:
        print("\n--- Gradebook System ---")
        user_input = input("Enter your Instructor ID (q for quit): ")
        if user_input == 'q':
            exit()

        instructor_id = int(user_input)
        instructor = Instructor(instructor_id)

        if not instructor.is_authenticated():
            print(Fore.RED + "Invalid Instructor ID. Try again. (q for quit)" + Style.RESET_ALL)
            continue

        instructor.display_courses()

        while True:
            course_id = input("Enter Course ID (q for quit): ")
            if course_id == 'q':
                exit()

            if not instructor.has_access(course_id):
                print("Invalid Course ID or Access Denied.")
                continue
            break;
        

        while True:
            print(f"\nSelected Course: {course_id}: {COURSES[course_id]["name"]}")
            print("\n1. Add Grade")
            print("2. Edit Grade")
            print("3. View Grades")
            print("4. Logout")

            choice = input("Enter choice: ")

            if choice == "4":
                print("Logging out...")
                break

            if choice == "1":  # Add Grade
                print("Students in this course:")
                for sid in ROSTERS[course_id]:
                    print(f"- {sid})")

                student_id = int(input("Enter Student ID: "))
                grade = input("Enter Grade: ")

                if student_id in ROSTERS[course_id]:
                    gradebook.add_grade(instructor, course_id, student_id, grade)
                else:
                    print("Invalid Student ID.")

            elif choice == "2":  # Edit Grade
                student_id = int(input("Enter Student ID: "))
                new_grade = input("Enter New Grade: ")
                gradebook.edit_grade(instructor, course_id, student_id, new_grade)

            elif choice == "3":  # View Grades
                gradebook.view_grades(instructor, course_id)

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()