import pytest
from gradebook import Gradebook
class FakeInstructor:
    def has_access(self, course_id):
        return True

@pytest.fixture
def gradebook():
    return Gradebook()
def test_existing_grade_edit_prompt(monkeypatch, capsys, gradebook):
    #Arrange
    instructor = FakeInstructor()
    course_id = "CS101"
    student_id = "123"
    initial_grade = 85

    inputs = iter(["", "Y", ""])  

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))

    gradebook.add_grade(instructor, course_id, student_id, initial_grade)  # First add
    gradebook.add_grade(instructor, course_id, student_id, 95)  # Should prompt and accept "Y"
    #Act
    captured = capsys.readouterr()
    #Assert
    assert "Grade updated for student" in captured.out
    assert gradebook.grades[course_id][student_id]["grade"] == 95
