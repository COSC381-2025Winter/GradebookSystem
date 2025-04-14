import pytest
from gradebook import Gradebook

@pytest.fixture
def gradebook():
    return Gradebook()

def test_edit_grade_prompt(monkeypatch, gradebook):
    # Arrange
    class Instructor:
        def has_access(self, course_id):
            return True

    instructor = Instructor()
    course_id = "CS101"
    student_id = "123"
    initial_grade = 85

    
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "Y")
    gradebook.add_grade(instructor, course_id, student_id, initial_grade)

    gradebook.add_grade(instructor, course_id, student_id, initial_grade)

    # Act: edit the grade
    gradebook.edit_grade(instructor, course_id, student_id, 95)

    # Assert
    updated_grade = gradebook.grades[course_id][student_id]["grade"]
    assert updated_grade == 95
