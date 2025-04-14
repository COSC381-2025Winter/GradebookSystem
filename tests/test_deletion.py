import pytest
from gradebook import Gradebook
from unittest.mock import patch

class MockInstructor:
    def __init__(self, accessible_courses):
        self.accessible_courses = accessible_courses

    def has_access(self, course_id):
        return course_id in self.accessible_courses

@pytest.fixture
def gradebook():
    return Gradebook()

@patch("builtins.input", return_value="")  # patch input() for testing
def test_delete_existing_grade(mock_input, gradebook):
    instructor = MockInstructor(["CS101"])
    gradebook.add_grade(instructor, "CS101", "student1", 90)

    result = gradebook.delete_grade(instructor, "CS101", "student1")

    assert result is True
    assert "CS101" not in gradebook.grades or "student1" not in gradebook.grades.get("CS101", {})

def test_delete_nonexistent_grade(gradebook):
    instructor = MockInstructor(["CS101"])

    result = gradebook.delete_grade(instructor, "CS101", "student999")

    assert result is False

@patch("builtins.input", return_value="")
def test_delete_no_access(mock_input, gradebook):
    instructor = MockInstructor([])  # No access
    authorized_instructor = MockInstructor(["CS101"])
    gradebook.add_grade(authorized_instructor, "CS101", "student1", 95)

    result = gradebook.delete_grade(instructor, "CS101", "student1")

    assert result is False
    assert "student1" in gradebook.grades["CS101"]

