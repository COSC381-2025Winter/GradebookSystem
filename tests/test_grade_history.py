import pytest
import datetime
from gradebook import Gradebook

class MockInstructor:
    def has_access(self, course_id):
        return course_id == "CS101"

# Mock data
mock_courses = {"CS101": {"name": "Intro to CS"}}
mock_students = {101: "John Doe", 102: "Jane Smith"}
mock_rosters = {"CS101": [101, 102]}

@pytest.fixture
def test_setup(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    monkeypatch.setattr('gradebook.COURSES', mock_courses)
    monkeypatch.setattr('gradebook.STUDENTS', mock_students)
    monkeypatch.setattr('gradebook.ROSTERS', mock_rosters)
    
    # Objects for testing
    gradebook = Gradebook()
    instructor = MockInstructor()
    return gradebook, instructor

def test_grade_history_initialization(test_setup):
  # Test that grade_history is properly initialized
    gradebook, _ = test_setup
    assert hasattr(gradebook, 'grade_history')
    assert isinstance(gradebook.grade_history, dict)

def test_add_grade_creates_history(test_setup):
    """Test that adding a grade creates a history entry"""
    gradebook, instructor = test_setup
    
    # Add a grade
    gradebook.add_grade(instructor, "CS101", 101, 85.0)
    
    # Check history was created
    assert "CS101" in gradebook.grade_history
    assert 101 in gradebook.grade_history["CS101"]
    assert len(gradebook.grade_history["CS101"][101]) == 1
    assert gradebook.grade_history["CS101"][101][0]["grade"] == 85.0

def test_edit_grade_adds_to_history(test_setup):
    # Test that editing a grade adds a new history entry
    gradebook, instructor = test_setup
    
    gradebook.add_grade(instructor, "CS101", 101, 85.0)
    gradebook.edit_grade(instructor, "CS101", 101, 90.0)
    
    history = gradebook.grade_history["CS101"][101]
    assert len(history) == 2
    assert history[0]["grade"] == 85.0
    assert history[1]["grade"] == 90.0

def test_view_grade_history_output(test_setup, capsys):
    #  Test the output when viewing grade history
    gradebook, instructor = test_setup

    gradebook.add_grade(instructor, "CS101", 101, 85.0)
    fixed_time = datetime.datetime(2025, 3, 15, 10, 0, 0)
    gradebook.grade_history["CS101"][101][0]["timestamp"] = fixed_time
    
    gradebook.view_grade_history(instructor, "CS101", 101)
    
    captured = capsys.readouterr()
    assert "John Doe (101)" in captured.out
    assert "Grade: 85.0" in captured.out
    assert "2025-03-15 10:00:00" in captured.out