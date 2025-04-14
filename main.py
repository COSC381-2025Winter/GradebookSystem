from util import clear_screen
from data import INSTRUCTORS, COURSES, STUDENTS, ROSTERS
from gradebook import Gradebook
from instructor import Instructor

def main():
    gradebook = Gradebook()
    
    # Instructor login loop
    while True:
        clear_screen()
        print("\n--- Gradebook System ---")
        user_input = input("Enter your Instructor ID (q for quit): ")
        if user_input.lower() == 'q':
            clear_screen()
            exit()
        if not user_input.isnumeric():
            print("\033[91mInvalid Instructor ID. Try again. (q for quit)\033[0m")
            continue
        instructor_id = int(user_input)
        instructor = Instructor(instructor_id)
        if not instructor.is_authenticated():
            print("\033[91mInvalid Instructor ID. Try again. (q for quit)\033[0m")
            continue
        
        # Course selection loop
        while True:
            clear_screen()
            instructor.display_courses()
            course_id_input = input("Enter Course ID (q for quit): ")
            if course_id_input.lower() == 'q':
                clear_screen()
                exit()
            course_id = course_id_input.upper()
            if not instructor.has_access(course_id):
                print("\033[91mInvalid Course ID or Access Denied.\033[0m")
                continue
            break  # Valid course selected
        
        # Course menu loop – note the menu text exactly matches what tests expect.
        while True:
            clear_screen()
            print("\n1. add grade")
            print("2. edit grade")
            print("3. view grades")
            print("4. sort grades")
            print("x. logout")
            
            choice = input("Enter choice: ")
            
            if choice == "x":
                break  # Exit to course selection (or re-login)
            
            elif choice == "1":
                clear_screen()
                print("Students in this course:")
                for sid in ROSTERS[course_id]:
                    print(f"- {STUDENTS.get(sid, 'Unknown')} (ID: {sid})")
                try:
                    student_id = int(input("Enter Student ID: "))
                except ValueError:
                    print("\033[91mInvalid student ID.\033[0m")
                    continue
                
                # Grade input loop – repeats until a non-empty grade is entered.
                while True:
                    grade = input("Enter Grade: ")
                    if not grade.strip():
                        print("\tGrade cannot be empty")
                    else:
                        break
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
                except ValueError:
                    print("\033[91mInvalid input.\033[0m")
                    continue
                gradebook.edit_grade(instructor, course_id, student_id, new_grade)
            
            elif choice == "3":
                clear_screen()
                gradebook.view_grades(instructor, course_id)
            
            elif choice == "4":
                clear_screen()
                inp = input("Would you like to sort by ascending or descending order? (a/d): ")
                inp = inp.lower()
                if inp in ['a', 'd']:
                    gradebook.sort_courses(inp)
                else:
                    print("Please type either (a/d)")
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()
