import pytest
from gradebook import Gradebook
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
    return Gradebook()


def test_ascending_list(test_grades):
    test_grades.sort_courses('a')
    assert test_grades.grades["CS101"] == {
        "202": {"grade": "A", "timestamp": ""},
        "203": {"grade": "C", "timestamp": ""},
        "201": {"grade": "D", "timestamp": ""}
    }

def test_descending_list(test_grades):
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


def test_negative_grade_input(monkeypatch, capsys):
    inputs = iter([
        '1',        # Instructor ID
        'light',    # Theme
        'CS101',    # Course ID
        '1',        # Add Grade
        'n',        # Skip search
        '201',      # Student ID
        '-50',      # Negative grade
        '',         # Enter after error
        'x',        # Switch Course
        '',         # Enter after switch
        'l',        # Logout
        ''          # Enter after logout
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main.clear_screen', lambda: None)

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

    main()
    captured = capsys.readouterr()
    assert "Grade cannot be negative" in captured.out


def test_non_numeric_grade_input(monkeypatch, capsys):
    inputs = iter([
        '1',        # Instructor ID
        'light',    # Theme
        'CS101',    # Course ID
        '1',        # Add Grade
        'n',        # Skip search
        '201',      # Student ID
        'abc',      # Invalid grade
        '',         # Enter after error
        'x',        # Switch Course
        '',         # Enter after switch
        'l',        # Logout
        ''          # Enter after logout
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main.clear_screen', lambda: None)

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

    main()
    captured = capsys.readouterr()
    assert "Invalid grade format" in captured.out