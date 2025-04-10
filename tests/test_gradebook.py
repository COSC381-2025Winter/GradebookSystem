import pytest
from gradebook import Gradebook
from instructor import Instructor

class MockInstructor:
    def __init__(self, instructor_id):
        self.instructor_id = instructor_id

    def has_access(self, course_id):
        return True  # Allow all access for testing

# Test numeric to letter grade conversion
@pytest.mark.parametrize("numeric, expected", [
    (100, 'A+'), (97, 'A+'),
    (95, 'A'), (93, 'A'),
    (91, 'A−'), (90, 'A−'),
    (88, 'B+'), (85, 'B'), (81, 'B−'),
    (78, 'C+'), (75, 'C'), (71, 'C−'),
    (68, 'D+'), (65, 'D'), (60, 'D−'),
    (59, 'F'), (0, 'F')
])
def test_letter_grade_conversion(numeric, expected):
    gradebook = Gradebook()
    assert gradebook.convert_to_letter_grade(numeric) == expected

# Test adding a valid grade
def test_add_valid_grade(capsys):
    gb = Gradebook()
    instructor = MockInstructor(101)
    course_id = "CS101"
    student_id = 201
    grade = 85

    gb.add_grade(instructor, course_id, student_id, grade)
    assert student_id in gb.grades[course_id]
    assert gb.grades[course_id][student_id]["grade"] == grade

    captured = capsys.readouterr()
    assert "grade added" in captured.out.lower()

# Test adding an invalid (non-integer) grade
def test_add_invalid_grade(capsys):
    gb = Gradebook()
    instructor = MockInstructor(101)
    course_id = "CS101"
    student_id = 201
    bad_grade = "ninety"

    gb.add_grade(instructor, course_id, student_id, bad_grade)
    captured = capsys.readouterr()
    assert "must be an integer" in captured.out.lower()
    assert student_id not in gb.grades.get(course_id, {})

# Test adding an out-of-range grade
@pytest.mark.parametrize("grade", [-10, 150])
def test_add_out_of_range_grade(capsys, grade):
    gb = Gradebook()
    instructor = MockInstructor(101)
    course_id = "CS101"
    student_id = 201

    gb.add_grade(instructor, course_id, student_id, grade)
    captured = capsys.readouterr()
    assert "between 0 and 100" in captured.out.lower()
    assert student_id not in gb.grades.get(course_id, {})

# Test editing grade after adding it
def test_edit_grade_within_7_days(capsys):
    gb = Gradebook()
    instructor = MockInstructor(101)
    course_id = "CS101"
    student_id = 201

    gb.add_grade(instructor, course_id, student_id, 85)
    gb.edit_grade(instructor, course_id, student_id, 90)

    assert gb.grades[course_id][student_id]["grade"] == 90

    captured = capsys.readouterr()
    assert "grade updated" in captured.out.lower()