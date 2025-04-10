from gradebook import Gradebook
import pytest
from main import main

@pytest.fixture
def test_grades():
    gb = Gradebook()
    gb.grades = {
        "CS101": {
            "201": {"grade": "D", "timestamp": ""},
            "202": {"grade": "A", "timestamp": ""},
            "203": {"grade": "C", "timestamp": ""}
        }
    }
    return gb

@pytest.fixture
def empty_grades():
    gb = Gradebook()
    return gb

def test_asecending_list(test_grades):
    test_grades.sort_courses('a')

    assert test_grades.grades["CS101"] == {
        "202": {"grade": "A", "timestamp": ""},
        "203": {"grade": "C", "timestamp": ""},
        "201": {"grade": "D", "timestamp": ""}
    }
    
def test_decending_list(test_grades):
    test_grades.sort_courses('d')

    assert test_grades.grades["CS101"] == {
        "201": {"grade": "D", "timestamp": ""},
        "203": {"grade": "C", "timestamp": ""},
        "202": {"grade": "A", "timestamp": ""}
        }
    
def test_bad_input(test_grades, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')

    test_grades.sort_courses('q')

    captured = capsys.readouterr()

    assert "Please type either (a/d)" in captured.out

def test_empty_input(empty_grades, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')

    empty_grades.sort_courses('a')

    captured = capsys.readouterr()

    assert "Grades are empty. Please add a grade" in captured.out

# Test case: entering a negative grade should trigger validation error
def test_negative_grade_input(monkeypatch, capsys):
    # Simulated user input sequence:
    # Navigates through login, selects a course, attempts to add a negative grade
    inputs = iter([
        '1',        # Instructor ID (valid)
        'CS101',    # Course ID (valid)
        '1',        # Menu option: Add Grade
        '201',      # Student ID
        '-50',      # ❌ Invalid negative grade
        '',         # Press enter after error message
        'x',        # Menu option: Logout
        '',         # Press enter after logout
        'q'         # Quit loop to exit main()
    ])

    # Mock input to simulate user interaction
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Prevent screen clearing during test
    monkeypatch.setattr('main.clear_screen', lambda: None)

    # Fake instructor object with proper authentication and course access
    class FakeInstructor:
        def __init__(self, instructor_id):
            self.instructor_id = instructor_id
            self.name = "Test Instructor"
            self.courses = {"CS101": "Intro to CS"}  # Give access to CS101
        def is_authenticated(self): return True
        def has_access(self, course_id): return course_id in self.courses
        def display_courses(self):
            print(f"Courses for {self.name}:")
            for cid, cname in self.courses.items():
                print(f"{cid}: {cname}")

    # Replace real Instructor class with our test version
    monkeypatch.setattr('main.Instructor', FakeInstructor)

    # Expect program to exit (due to user choosing logout -> quit)
    with pytest.raises(SystemExit):
        main()

    # Capture and assert the expected error message
    captured = capsys.readouterr()
    assert "Grade cannot be negative" in captured.out


# Test case: entering a non-numeric grade should trigger validation error
def test_non_numeric_grade_input(monkeypatch, capsys):
    # Simulated user input sequence:
    inputs = iter([
        '1',        # Instructor ID
        'CS101',    # Course ID
        '1',        # Add Grade
        '201',      # Student ID
        'abc',      # ❌ Invalid non-numeric input
        '',         # Press enter after error
        'x',        # Logout
        '',         # Press enter after logout
        'q'         # Quit loop to end test
    ])

    # Patch input and screen clearing
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main.clear_screen', lambda: None)

    # Reuse same instructor mocking
    class FakeInstructor:
        def __init__(self, instructor_id):
            self.instructor_id = instructor_id
            self.name = "Test Instructor"
            self.courses = {"CS101": "Intro to CS"}
        def is_authenticated(self): return True
        def has_access(self, course_id): return course_id in self.courses
        def display_courses(self):
            print(f"Courses for {self.name}:")
            for cid, cname in self.courses.items():
                print(f"{cid}: {cname}")

    monkeypatch.setattr('main.Instructor', FakeInstructor)

    with pytest.raises(SystemExit):
        main()

    # Assert expected message was printed
    captured = capsys.readouterr()
    assert "Invalid grade format" in captured.out

import pytest
from gradebook import Gradebook
from instructor import Instructor

class MockInstructor:
    def __init__(self, instructor_id):
        self.instructor_id = instructor_id

    def has_access(self, course_id):
        return True  # Allow all access for testing

# Test numeric to letter grade conversion
@pytest.mark.parametrize("numeric, expected", [
    (100, 'A+'), (97, 'A+'),
    (95, 'A'), (93, 'A'),
    (91, 'A−'), (90, 'A−'),
    (88, 'B+'), (85, 'B'), (81, 'B−'),
    (78, 'C+'), (75, 'C'), (71, 'C−'),
    (68, 'D+'), (65, 'D'), (60, 'D−'),
    (59, 'F'), (0, 'F')
])
def test_letter_grade_conversion(numeric, expected):
    gradebook = Gradebook()
    assert gradebook.convert_to_letter_grade(numeric) == expected

# Test adding a valid grade
def test_add_valid_grade(capsys):
    gb = Gradebook()
    instructor = MockInstructor(101)
    course_id = "CS101"
    student_id = 201
    grade = 85

    gb.add_grade(instructor, course_id, student_id, grade)
    assert student_id in gb.grades[course_id]
    assert gb.grades[course_id][student_id]["grade"] == grade

    captured = capsys.readouterr()
    assert "grade added" in captured.out.lower()

# Test adding an invalid (non-integer) grade
def test_add_invalid_grade(capsys):
    gb = Gradebook()
    instructor = MockInstructor(101)
    course_id = "CS101"
    student_id = 201
    bad_grade = "ninety"

    gb.add_grade(instructor, course_id, student_id, bad_grade)
    captured = capsys.readouterr()
    assert "must be an integer" in captured.out.lower()
    assert student_id not in gb.grades.get(course_id, {})

# Test adding an out-of-range grade
@pytest.mark.parametrize("grade", [-10, 150])
def test_add_out_of_range_grade(capsys, grade):
    gb = Gradebook()
    instructor = MockInstructor(101)
    course_id = "CS101"
    student_id = 201

    gb.add_grade(instructor, course_id, student_id, grade)
    captured = capsys.readouterr()
    assert "between 0 and 100" in captured.out.lower()
    assert student_id not in gb.grades.get(course_id, {})

# Test editing grade after adding it
def test_edit_grade_within_7_days(capsys):
    gb = Gradebook()
    instructor = MockInstructor(101)
    course_id = "CS101"
    student_id = 201

    gb.add_grade(instructor, course_id, student_id, 85)
    gb.edit_grade(instructor, course_id, student_id, 90)

    assert gb.grades[course_id][student_id]["grade"] == 90

    captured = capsys.readouterr()
    assert "grade updated" in captured.out.lower()