import pytest
from gradebook import Gradebook
import datetime

import builtins
builtins.input = lambda _: None

#Mock Setup
class MockInstructor:
    def __init__(self, instructor_id):
        self.instructor_id = instructor_id

    def has_access(self, course_id):
        return True  

#Fixtures
@pytest.fixture
def gradebook():
    return Gradebook()

@pytest.fixture
def instructor():
    return MockInstructor(101)

@pytest.fixture
def sample_course():
    return "CS101"

@pytest.fixture
def sample_student():
    return 201

#convert_to_letter_grade tests
@pytest.mark.parametrize("numeric, expected", [
    (100, 'A+'), (97, 'A+'),
    (94, 'A'), (90, 'A−'),
    (88, 'B+'), (84, 'B'), (80, 'B−'),
    (77, 'C+'), (73, 'C'), (70, 'C−'),
    (67, 'D+'), (63, 'D'), (60, 'D−'),
    (59, 'F'), (0, 'F')
])
def test_convert_to_letter_grade(gradebook, numeric, expected):
    # Act
    result = gradebook.convert_to_letter_grade(numeric)

    # Assert
    assert result == expected

#add_grade tests
def test_add_valid_grade(gradebook, instructor, sample_course, sample_student, capsys):
    # Act
    gradebook.add_grade(instructor, sample_course, sample_student, 85)

    # Assert
    assert sample_student in gradebook.grades[sample_course]
    assert gradebook.grades[sample_course][sample_student]["grade"] == 85

    captured = capsys.readouterr()
    assert "grade added" in captured.out.lower()

def test_add_invalid_grade_non_integer(gradebook, instructor, sample_course, sample_student, capsys):
    # Act
    gradebook.add_grade(instructor, sample_course, sample_student, "ninety")

    # Assert
    assert sample_student not in gradebook.grades.get(sample_course, {})

    captured = capsys.readouterr()
    assert "must be an integer" in captured.out.lower()

@pytest.mark.parametrize("grade", [-10, 150])
def test_add_invalid_out_of_range_grade(gradebook, instructor, sample_course, sample_student, grade, capsys):
    # Act
    gradebook.add_grade(instructor, sample_course, sample_student, grade)

    # Assert
    assert sample_student not in gradebook.grades.get(sample_course, {})

    captured = capsys.readouterr()
    assert "between 0 and 100" in captured.out.lower()

# edit_grade tests 
def test_edit_grade_within_7_days(gradebook, instructor, sample_course, sample_student, capsys):
    # Arrange
    gradebook.add_grade(instructor, sample_course, sample_student, 85)

    # Act
    gradebook.edit_grade(instructor, sample_course, sample_student, 90)

    # Assert
    assert gradebook.grades[sample_course][sample_student]["grade"] == 90

    captured = capsys.readouterr()
    assert "grade updated" in captured.out.lower()
