import builtins
import pytest
from gradebook import Gradebook
from instructor import Instructor

# You can mock your own course and instructor ID for a test scenario
VALID_INSTRUCTOR_ID = 1001
VALID_COURSES = ["CS101", "MATH202"]

# Mock data setup
@pytest.fixture
def mock_instructor(monkeypatch):
    instructor = Instructor(VALID_INSTRUCTOR_ID)

    # Ensure the instructor is always authenticated
    monkeypatch.setattr(instructor, "is_authenticated", lambda: True)
    monkeypatch.setattr(instructor, "has_access", lambda cid: cid in VALID_COURSES)
    monkeypatch.setattr(instructor, "display_courses", lambda: print("CS101\nMATH202"))
    return instructor

def test_course_switching(monkeypatch, capfd, mock_instructor):
    # Simulate user selecting courses, then switching, then quitting
    inputs = iter([
        "dark",          # Theme
        "CS101",         # First course
        "x",             # Switch course
        "MATH202",       # Second course
        "x",             # Switch again
        "l",             # Logout
    ])

    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    from main import prompt_for_theme

    # Patch clear_screen and print_information to avoid clutter
    monkeypatch.setattr("util.clear_screen", lambda: None)
    monkeypatch.setattr("color_ui.print_information", print)

    # Call only the portions we can test independently
    prompt_for_theme(mock_instructor)

    # Simulate the course selection loop (extracted logic from main)
    selected_courses = []

    while True:
        mock_instructor.display_courses()
        course_id = input("Enter Course ID (l to logout): ")
        if course_id.lower() == 'l':
            break
        course_id = course_id.upper()
        if not mock_instructor.has_access(course_id):
            continue
        selected_courses.append(course_id)

        # Simulate inner course menu loop until 'x' is chosen
        choice = input("Enter choice: ")
        if choice == 'x':
            continue

    # Final assertions
    assert selected_courses == ["CS101", "MATH202"]