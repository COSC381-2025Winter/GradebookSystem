import datetime
import pytest
from gradebook import Gradebook


class MockInstructor:
    def has_access(self, course_id):
        return True


@pytest.fixture
def setup_gradebook():
    gb = Gradebook()
    instructor = MockInstructor()
    course_id = "CS101"
    student_id = "stu123"
    gb.grades[course_id] = {
        student_id: {
            "grade": 85,
            "timestamp": datetime.datetime.now() - datetime.timedelta(days=2)
        }
    }
    return gb, instructor, course_id, student_id


def test_edit_grade_confirm_yes(monkeypatch, capsys, setup_gradebook):
    gb, instructor, course_id, student_id = setup_gradebook

    # Create a list of inputs and simulate responses one by one
    responses = iter(['y' if "change it to" in prompt else ''])  # Simulate 'y' confirmation for grade change
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))  # Ensure the response is always taken from 'responses'

    gb.edit_grade(instructor, course_id, student_id, 95)
    captured = capsys.readouterr()

    assert f"Current Grade for Student {student_id}: 85" in captured.out
    assert f"Grade updated for student {student_id}: 95" in captured.out
    assert gb.grades[course_id][student_id]["grade"] == 95


def test_edit_grade_confirm_no(monkeypatch, capsys, setup_gradebook):
    gb, instructor, course_id, student_id = setup_gradebook

    # Create a list of inputs and simulate responses one by one
    responses = iter(['n' if "change it to" in prompt else ''])  # Simulate 'n' cancellation for grade change
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))  # Ensure the response is always taken from 'responses'

    gb.edit_grade(instructor, course_id, student_id, 95)
    captured = capsys.readouterr()

    assert "Grade update canceled." in captured.out
    assert gb.grades[course_id][student_id]["grade"] == 85


def test_edit_grade_input_enter(monkeypatch, capsys, setup_gradebook):
    gb, instructor, course_id, student_id = setup_gradebook

    # Create a list of inputs and simulate just pressing enter (empty string)
    responses = iter([''])  # Simulate an empty response (pressing enter)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))  # Ensure the response is always taken from 'responses'

    gb.edit_grade(instructor, course_id, student_id, 95)
    captured = capsys.readouterr()

    assert "Grade update canceled." in captured.out
    assert gb.grades[course_id][student_id]["grade"] == 85


def test_edit_grade_expired_window(monkeypatch, capsys):
    gb = Gradebook()
    instructor = MockInstructor()
    course_id = "CS101"
    student_id = "stu123"

    # Set grade with timestamp older than 7 days
    gb.grades[course_id] = {
        student_id: {
            "grade": 75,
            "timestamp": datetime.datetime.now() - datetime.timedelta(days=10)
        }
    }

    # Create a list of inputs (it won't matter here, so we use an empty response)
    responses = iter([''])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))

    gb.edit_grade(instructor, course_id, student_id, 95)
    captured = capsys.readouterr()

    assert "Error: Grade editing period (7 days) has expired." in captured.out
    assert gb.grades[course_id][student_id]["grade"] == 75


def test_edit_grade_no_existing_grade(monkeypatch, capsys):
    gb = Gradebook()
    instructor = MockInstructor()
    course_id = "CS101"
    student_id = "stu999"  # no entry

    # Create a list of inputs (it won't matter here, so we use an empty response)
    responses = iter([''])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))

    gb.edit_grade(instructor, course_id, student_id, 88)
    captured = capsys.readouterr()

    assert "Error: No existing grade found. Use 'add' instead." in captured.out
    assert student_id not in gb.grades.get(course_id, {})
