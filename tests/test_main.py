import datetime
import pytest
from instructor import Instructor
from gradebook import Gradebook
from data import INSTRUCTORS, STUDENTS, COURSES, ROSTERS
from main import main

import builtins
builtins.input = lambda _: '\n'

def test_data_instructors():
    assert 101 in INSTRUCTORS
    assert INSTRUCTORS[101] == "Dr. Smith"

def test_data_students():
    assert STUDENTS[201] == "Alice"

def test_data_courses():
    assert COURSES["CS101"]["instructor_id"] == 101

def test_data_rosters():
    assert 201 in ROSTERS["CS101"]

def test_instructor_authentication():
    instructor = Instructor(101)
    assert instructor.is_authenticated()

def test_invalid_instructor():
    bad = Instructor(999)
    assert not bad.is_authenticated()

@pytest.fixture
def test_instructor():
    return Instructor(101)

def test_add_and_view_grade(monkeypatch, capsys, test_instructor):
    gb = Gradebook()
    course_id = "CS101"
    student_id = 201
    monkeypatch.setattr('builtins.input', lambda _: '\n')
    gb.add_grade(test_instructor, course_id, student_id, 95, force=True)
    gb.view_grades(test_instructor, course_id)
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "95" in captured.out

def test_edit_grade_within_7_days(monkeypatch, test_instructor):
    gb = Gradebook()
    course_id = "CS101"
    student_id = 202
    gb.add_grade(test_instructor, course_id, student_id, 70, force=True)
    gb.edit_grade(test_instructor, course_id, student_id, 85)
    assert gb.grades[course_id][student_id]["grade"] == 85

def test_edit_grade_after_7_days(monkeypatch, test_instructor):
    gb = Gradebook()
    course_id = "CS101"
    student_id = 203
    gb.add_grade(test_instructor, course_id, student_id, 75, force=True)
    gb.grades[course_id][student_id]["timestamp"] = datetime.datetime.now() - datetime.timedelta(days=8)
    gb.edit_grade(test_instructor, course_id, student_id, 100)
    assert gb.grades[course_id][student_id]["grade"] == 75

def test_login_with_invalid_id(monkeypatch, capsys):
    responses = iter(['10', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses, 'q'))
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "instructor id" in captured.out.lower()

