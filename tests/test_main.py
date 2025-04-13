import datetime
import pytest

# Mock Data
INSTRUCTORS = {
    101: "Dr. Smith",
}

STUDENTS = {
    201: "Alice",
    202: "Bob",
    203: "Charlie",
    204: "David",
}

COURSES = {
    "CS101": {"name": "Intro to CS", "instructor_id": 101},
    "CS111": {"name": "Java Programming", "instructor_id": 101}
}

ROSTERS = {
    "CS101": [201, 202],
    "CS111": [203, 204]
}

# Mock Print Functions
def print_success(msg): pass
def print_error(msg): pass
def print_information(msg): pass
def print_warning(msg): pass

# Instructor class
class Instructor:
    def __init__(self, instructor_id):
        self.instructor_id = instructor_id
        self.name = INSTRUCTORS.get(instructor_id)
        self.courses = {cid: COURSES[cid]["name"] for cid in COURSES if COURSES[cid]["instructor_id"] == instructor_id}

    def is_authenticated(self):
        return self.name is not None

    def has_access(self, course_id):
        return course_id in self.courses

    def display_courses(self):
        return list(self.courses.keys())

# Gradebook class
class Gradebook:
    def __init__(self):
        self.grades = {}  # {course_id: {student_id: {"grade": x, "timestamp": y}}}

    def add_grade(self, instructor, course_id, student_id, grade, force=False):
        if not instructor.has_access(course_id):
            return "Access Denied"
        if course_id not in self.grades:
            self.grades[course_id] = {}
        now = datetime.datetime.now()
        if student_id in self.grades[course_id] and not force:
            return "Grade already exists"
        self.grades[course_id][student_id] = {"grade": grade, "timestamp": now}
        return "Grade added"

    def edit_grade(self, instructor, course_id, student_id, new_grade):
        if not instructor.has_access(course_id):
            return "Access Denied"
        if course_id in self.grades and student_id in self.grades[course_id]:
            old_timestamp = self.grades[course_id][student_id]["timestamp"]
            now = datetime.datetime.now()
            if (now - old_timestamp).days <= 7:
                self.grades[course_id][student_id] = {"grade": new_grade, "timestamp": now}
                return "Grade updated"
            else:
                return "Edit window expired"
        else:
            return "No existing grade"

    def view_grades(self, instructor, course_id):
        if not instructor.has_access(course_id):
            return "Access Denied"
        return self.grades.get(course_id, {})

# Fixtures
@pytest.fixture
def instructor():
    return Instructor(101)

@pytest.fixture
def gradebook():
    return Gradebook()

# Tests
def test_add_grade_success(gradebook, instructor):
    result = gradebook.add_grade(instructor, "CS101", 201, 90)
    assert result == "Grade added"
    assert gradebook.grades["CS101"][201]["grade"] == 90

def test_add_duplicate_grade_without_force(gradebook, instructor):
    gradebook.add_grade(instructor, "CS101", 201, 90)
    result = gradebook.add_grade(instructor, "CS101", 201, 95)
    assert result == "Grade already exists"

def test_add_duplicate_grade_with_force(gradebook, instructor):
    gradebook.add_grade(instructor, "CS101", 201, 90)
    result = gradebook.add_grade(instructor, "CS101", 201, 95, force=True)
    assert result == "Grade added"
    assert gradebook.grades["CS101"][201]["grade"] == 95

def test_add_grade_access_denied(gradebook):
    other_instructor = Instructor(999)
    result = gradebook.add_grade(other_instructor, "CS101", 202, 80)
    assert result == "Access Denied"

def test_edit_grade_success(gradebook, instructor):
    gradebook.add_grade(instructor, "CS101", 202, 88)
    result = gradebook.edit_grade(instructor, "CS101", 202, 93)
    assert result == "Grade updated"
    assert gradebook.grades["CS101"][202]["grade"] == 93

def test_edit_grade_expired(gradebook, instructor):
    gradebook.grades["CS101"] = {
        203: {"grade": 70, "timestamp": datetime.datetime.now() - datetime.timedelta(days=10)}
    }
    result = gradebook.edit_grade(instructor, "CS101", 203, 95)
    assert result == "Edit window expired"

def test_edit_grade_not_found(gradebook, instructor):
    result = gradebook.edit_grade(instructor, "CS101", 204, 85)
    assert result == "No existing grade"

def test_view_grades_success(gradebook, instructor):
    gradebook.add_grade(instructor, "CS101", 201, 77)
    grades = gradebook.view_grades(instructor, "CS101")
    assert 201 in grades
    assert grades[201]["grade"] == 77

def test_view_grades_access_denied(gradebook):
    other_instructor = Instructor(999)
    result = gradebook.view_grades(other_instructor, "CS101")
    assert result == "Access Denied"
