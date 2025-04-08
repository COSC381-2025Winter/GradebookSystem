import pytest
from main import main

def test_negative_grade_input(monkeypatch, capsys):
    inputs = iter([
        '1',        # Instructor ID
        'CS101',    # Course ID
        '1',        # Add Grade
        '201',      # Student ID
        '-50',      # Negative grade
        '',         # Press enter to continue
        '4',        # Logout
        '',         # Press enter to continue after logout
        'q'         # One extra input so main() can safely loop once more
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

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "Grade cannot be negative" in captured.out


def test_non_numeric_grade_input(monkeypatch, capsys):
    inputs = iter([
        '1',        # Instructor ID
        'CS101',    # Course ID
        '1',        # Add Grade
        '201',      # Student ID
        'abc',      # Invalid grade
        '',         # Press enter to continue
        '4',        # Logout
        '',         # Press enter to continue after logout
        'q'         # One extra input
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

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "Invalid grade format" in captured.out
