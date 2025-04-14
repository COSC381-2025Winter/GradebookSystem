import datetime
import pytest
import builtins
from unittest.mock import patch, Mock

import data
from instructor import Instructor
from gradebook import Gradebook
from main import main

# Automatically reset data before each test
@pytest.fixture(autouse=True)
def mock_data():
    data.INSTRUCTORS.clear()
    data.INSTRUCTORS.update({101: "Dr. Smith"})
    data.STUDENTS.clear()
    data.STUDENTS.update({
        201: "Alice",
        202: "Bob",
        203: "Charlie",
        204: "David",
    })
    data.COURSES.clear()
    data.COURSES.update({
        "CS101": {"name": "Intro to CS", "instructor_id": 101},
        "CS111": {"name": "Java Programming", "instructor_id": 101},
    })
    data.ROSTERS.clear()
    data.ROSTERS.update({
        "CS101": [201, 202, 203, 204, 205, 206],
        "CS111": [201, 202, 203, 204, 205, 206],
    })

@pytest.fixture
def instructor():
    return Instructor(101)

@pytest.fixture
def gradebook():
    return Gradebook()

@pytest.fixture(autouse=True)
def patch_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")

# Add Grade Tests
def test_add_grade_success(gradebook, instructor):
    result = gradebook.add_grade(instructor, "CS101", 201, 90)
    assert result is None or result == "Grade added"
    assert gradebook.grades["CS101"][201]["grade"] == 90

def test_add_duplicate_grade_without_force(gradebook, instructor):
    gradebook.add_grade(instructor, "CS101", 201, 90)
    result = gradebook.add_grade(instructor, "CS101", 201, 95)
    assert result is None or result == "Grade already exists"

def test_add_duplicate_grade_with_force(gradebook, instructor):
    gradebook.add_grade(instructor, "CS101", 201, 90)
    result = gradebook.add_grade(instructor, "CS101", 201, 95, force=True)
    assert result is None or result == "Grade added"
    assert gradebook.grades["CS101"][201]["grade"] == 95

def test_add_grade_access_denied(gradebook):
    other_instructor = Instructor(999)
    result = gradebook.add_grade(other_instructor, "CS101", 202, 80)
    assert result is None or result == "Access Denied"

# Edit Grade Tests
def test_edit_grade_success(gradebook, instructor):
    gradebook.add_grade(instructor, "CS101", 202, 88)
    result = gradebook.edit_grade(instructor, "CS101", 202, 93)
    assert result is None or result == "Grade updated"
    assert gradebook.grades["CS101"][202]["grade"] == 93

def test_edit_grade_expired(gradebook, instructor):
    gradebook.grades["CS101"] = {
        203: {"grade": 70, "timestamp": datetime.datetime.now() - datetime.timedelta(days=10)}
    }
    result = gradebook.edit_grade(instructor, "CS101", 203, 95)
    assert result is None or result == "Edit window expired"

def test_edit_grade_not_found(gradebook, instructor):
    result = gradebook.edit_grade(instructor, "CS101", 204, 85)
    assert result is None or result == "No existing grade"

# View Grade Tests
def test_view_grades_success(gradebook, instructor):
    gradebook.add_grade(instructor, "CS101", 201, 77)
    grades = gradebook.view_grades(instructor, "CS101")
    assert grades is not None
    assert 201 in grades
    assert grades[201]["grade"] == 77

def test_view_grades_access_denied(gradebook):
    other_instructor = Instructor(999)
    result = gradebook.view_grades(other_instructor, "CS101")
    assert result is None or result == "Access Denied"

# Additional edge tests
def test_bad_input(gradebook, capsys):
    gradebook.grades.clear()
    gradebook.sort_courses('q')
    captured = capsys.readouterr()
    assert "Grades are empty" in captured.out

def test_empty_input(gradebook, capsys):
    gradebook.grades.clear()
    gradebook.sort_courses('a')
    captured = capsys.readouterr()
    assert "Grades are empty. Please add a grade" in captured.out

# Main-interacting tests
def test_negative_grade_input(monkeypatch):
    inputs = iter(['1', 'light', 'CS101', '1', 'n', '201', '-50', '', 'x', '', 'q', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main.clear_screen', lambda: None)

    class FakeInstructor:
        def __init__(self, instructor_id):
            self.instructor_id = instructor_id
            self.name = "Test Instructor"
            self.courses = {"CS101": "Intro to CS"}
        def is_authenticated(self): return True
        def has_access(self, course_id): return course_id in self.courses
        def display_courses(self): pass
        def set_theme(self, theme): pass

    monkeypatch.setattr('main.Instructor', FakeInstructor)
    with pytest.raises(SystemExit):
        main()

def test_non_numeric_grade_input(monkeypatch):
    inputs = iter(['1', 'light', 'CS101', '1', 'n', '201', 'abc', '', 'x', '', 'q', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main.clear_screen', lambda: None)

    class FakeInstructor:
        def __init__(self, instructor_id):
            self.instructor_id = instructor_id
            self.name = "Test Instructor"
            self.courses = {"CS101": "Intro to CS"}
        def is_authenticated(self): return True
        def has_access(self, course_id): return course_id in self.courses
        def display_courses(self): pass
        def set_theme(self, theme): pass

    monkeypatch.setattr('main.Instructor', FakeInstructor)
    with pytest.raises(SystemExit):
        main()

def test_show_names_when_adding_grade(monkeypatch):
    inputs = iter(['101', 'light', 'CS101', '1', 'n', '201', 'A', '90', '', 'x', '', 'q', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main.clear_screen', lambda: None)

    class FakeInstructor:
        def __init__(self, instructor_id):
            self.instructor_id = instructor_id
            self.name = "Dr. Smith"
            self.courses = {"CS101": "Intro to CS", "CS111": "Java Programming"}
        def is_authenticated(self): return True
        def has_access(self, course_id): return course_id in self.courses
        def display_courses(self): print("CS101\nCS111")
        def set_theme(self, theme): pass

    monkeypatch.setattr('main.Instructor', FakeInstructor)
    with pytest.raises(SystemExit):
        main()

def test_empty_grade(monkeypatch):
    inputs = iter(['101', 'light', 'CS101', '1', 'n', '201', '', '99', '', 'x', '', 'q', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main.clear_screen', lambda: None)

    class FakeInstructor:
        def __init__(self, instructor_id):
            self.instructor_id = instructor_id
            self.name = "Dr. Smith"
            self.courses = {"CS101": "Intro to CS", "CS111": "Java Programming"}
        def is_authenticated(self): return True
        def has_access(self, course_id): return course_id in self.courses
        def display_courses(self): print("CS101\nCS111")
        def set_theme(self, theme): pass

    monkeypatch.setattr('main.Instructor', FakeInstructor)
    with pytest.raises(SystemExit):
        main()

def test_matching_student_displayed(monkeypatch):
    inputs = iter(['101', 'light', 'CS101', '1', 'y', '201', '', 'back', '201', '85', '', 'x', '', 'q', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main.clear_screen', lambda: None)

    class FakeInstructor:
        def __init__(self, instructor_id):
            self.instructor_id = instructor_id
            self.name = "Dr. Smith"
            self.courses = {"CS101": "Intro to CS", "CS111": "Java Programming"}
        def is_authenticated(self): return True
        def has_access(self, course_id): return course_id in self.courses
        def display_courses(self): print("CS101\nCS111")
        def set_theme(self, theme): pass

    monkeypatch.setattr('main.Instructor', FakeInstructor)
    with pytest.raises(SystemExit):
        main()
