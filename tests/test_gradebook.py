import pytest
import re
from gradebook import Gradebook
from main import main

def remove_ansi(text):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

@pytest.fixture
def test_grades():
    gb = Gradebook()
    gb.grades = {
        "CS101": {
            201: {"grade": 65.0, "timestamp": ""},
            202: {"grade": 95.0, "timestamp": ""},
            203: {"grade": 80.0, "timestamp": ""}
        }
    }
    return gb

@pytest.fixture
def empty_grades():
    return Gradebook()

def test_asecending_list(test_grades):
    test_grades.sort_courses('a')
    sorted_keys = list(test_grades.grades["CS101"].keys())
    assert sorted_keys == [202, 203, 201]  # highest to lowest (ascending)

def test_decending_list(test_grades):
    test_grades.sort_courses('d')
    sorted_keys = list(test_grades.grades["CS101"].keys())
    assert sorted_keys == [201, 203, 202]  # lowest to highest (descending)

def test_bad_input(test_grades, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    test_grades.sort_courses('q')
    captured = capsys.readouterr()
    assert "Please type either (a/d)" in captured.out

def test_empty_input(empty_grades, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    empty_grades.grades = {}
    empty_grades.sort_courses('a')
    captured = capsys.readouterr()
    output = remove_ansi(captured.out)
    assert "Grades are empty. Please add a grade" in output

def test_negative_grade_input(monkeypatch, capsys):
    inputs = iter([
        '1', 'light', 'CS101', '1', 'n', '201', '-50', '', 'x', '', 'q'
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
        '1', 'light', 'CS101', '1', 'n', '201', 'abc', '', 'x', '', 'q'
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
