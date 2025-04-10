import datetime
import pytest
from instructor import Instructor
from gradebook import Gradebook
from data import INSTRUCTORS, STUDENTS, COURSES, ROSTERS

# --- Setup: Mock input to suppress prompts during testing ---
import builtins
builtins.input = lambda _: '\n'  # Mock input for all input() calls during tests

# ----------------------------
# 🔍 Tests for data.py
# ----------------------------

def test_data_instructors():
    assert 101 in INSTRUCTORS
    assert INSTRUCTORS[101] == "Dr. Smith"
    assert 104 in INSTRUCTORS

def test_data_students():
    assert 201 in STUDENTS
    assert STUDENTS[201] == "Alice"
    assert STUDENTS[223] == "Wendy"

def test_data_courses():
    assert "CS101" in COURSES
    assert COURSES["CS101"]["instructor_id"] == 101
    assert COURSES["CS301"]["name"] == "Advanced Algorithms"

def test_data_rosters():
    assert "CS101" in ROSTERS
    assert 201 in ROSTERS["CS101"]
    assert len(ROSTERS["CS302"]) == 3

# ----------------------------
# 🔍 Tests for instructor.py
# ----------------------------

def test_instructor_authentication():
    instructor = Instructor(101)
    assert instructor.is_authenticated()
    assert instructor.name == "Dr. Smith"

def test_instructor_courses():
    instructor = Instructor(101)
    courses = instructor.get_courses()
    assert "CS101" in courses
    assert instructor.has_access("CS111")
    assert not instructor.has_access("CS202")

def test_invalid_instructor():
    fake = Instructor(999)
    assert not fake.is_authenticated()
    assert fake.courses == []

# ----------------------------
# 🔍 Tests for gradebook.py
# ----------------------------

@pytest.fixture
def test_instructor():
    return Instructor(101)

def test_add_and_view_grade(monkeypatch, capsys, test_instructor):
    gb = Gradebook()
    course_id = "CS101"
    student_id = 201

    # Simulate adding a grade
    monkeypatch.setattr('builtins.input', lambda _: '\n')
    gb.add_grade(test_instructor, course_id, student_id, 88, force=True)

    assert gb.grades[course_id][student_id]["grade"] == 88

    # View grades and capture the output
    gb.view_grades(test_instructor, course_id)
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "88" in captured.out

def test_edit_grade_within_7_days(monkeypatch, test_instructor):
    gb = Gradebook()
    course_id = "CS101"
    student_id = 202
    gb.add_grade(test_instructor, course_id, student_id, 70, force=True)
    
    monkeypatch.setattr('builtins.input', lambda _: '\n')
    gb.edit_grade(test_instructor, course_id, student_id, 95)
    assert gb.grades[course_id][student_id]["grade"] == 95

def test_edit_grade_after_7_days(monkeypatch, test_instructor):
    gb = Gradebook()
    course_id = "CS101"
    student_id = 203
    gb.add_grade(test_instructor, course_id, student_id, 75, force=True)

    # Set timestamp to 8 days ago
    gb.grades[course_id][student_id]["timestamp"] = datetime.datetime.now() - datetime.timedelta(days=8)

    monkeypatch.setattr('builtins.input', lambda _: '\n')
    gb.edit_grade(test_instructor, course_id, student_id, 100)

    # Grade should not be updated due to time restriction
    assert gb.grades[course_id][student_id]["grade"] == 75
