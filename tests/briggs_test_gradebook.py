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

    # Simulate confirmation = 'y', then enter
    monkeypatch.setattr("builtins.input", lambda prompt="": 'y' if "change it to" in prompt else "")

    gb.edit_grade(instructor, course_id, student_id, 95)
    captured = capsys.readouterr()

    assert f"Current Grade for Student {student_id}: 85" in captured.out
    assert f"Grade updated for student {student_id}: 95" in captured.out
    assert gb.grades[course_id][student_id]["grade"] == 95


def test_edit_grade_confirm_no(monkeypatch, capsys, setup_gradebook):
    gb, instructor, course_id, student_id = setup_gradebook

    # Simulate confirmation = 'n', then enter
    monkeypatch.setattr("builtins.input", lambda prompt="": 'n' if "change it to" in prompt else "")

    gb.edit_grade(instructor, course_id, student_id, 95)
    captured = capsys.readouterr()

    assert "Grade update canceled." in captured.out
    assert gb.grades[course_id][student_id]["grade"] == 85


def test_edit_grade_input_enter(monkeypatch, capsys, setup_gradebook):
    gb, instructor, course_id, student_id = setup_gradebook

    # Simulate just pressing enter (input is empty string)
    monkeypatch.setattr("builtins.input", lambda prompt="": "")

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

    monkeypatch.setattr("builtins.input", lambda prompt="": "")  # doesn't matter, will be skipped

    gb.edit_grade(instructor, course_id, student_id, 95)
    captured = capsys.readouterr()

    assert "Error: Grade editing period (7 days) has expired." in captured.out
    assert gb.grades[course_id][student_id]["grade"] == 75


def test_edit_grade_no_existing_grade(monkeypatch, capsys):
    gb = Gradebook()
    instructor = MockInstructor()
    course_id = "CS101"
    student_id = "stu999"  # no entry

    monkeypatch.setattr("builtins.input", lambda prompt="": "")  # doesn't matter

    gb.edit_grade(instructor, course_id, student_id, 88)
    captured = capsys.readouterr()

    assert "Error: No existing grade found. Use 'add' instead." in captured.out
    assert student_id not in gb.grades.get(course_id, {})