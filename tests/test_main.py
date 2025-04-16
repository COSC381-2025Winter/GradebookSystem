import datetime
from unittest.mock import patch, Mock
from main import main
from instructor import Instructor
from gradebook import Gradebook
import pytest
import builtins

@pytest.fixture
def test_instructor():
    return {
        "id": 101,
        "name": "Dr. Smith",
        "courses": ["CS101", "CS111"],
        "invalid_course": "CSabc"
    }

# --- LOGOUT TEST ---

@pytest.mark.parametrize("logout_input", ['l', 'L'])
def test_logout_on_course_id_input(monkeypatch, capsys, logout_input):
    # Add extra inputs to avoid StopIteration
    inputs = iter(['101', 'light', logout_input, '', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with pytest.raises(SystemExit) as exitInfo:
        main()

    captured = capsys.readouterr()
    assert "logging out" in captured.out.lower()

# --- LOGIN VALIDITY TESTS ---

def test_login_with_invalid_id(monkeypatch, capsys):
    responses = iter(['10', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert 'instructor id' in captured.out.lower()

def test_login_with_valid_id(monkeypatch, capsys, test_instructor):
    mock_datetime = Mock()
    mock_datetime.now.return_value = datetime.datetime(2024, 9, 15)
    monkeypatch.setattr('instructor.datetime.datetime', mock_datetime)
    responses = iter([str(test_instructor["id"]), 'light', 'l', '', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()
    captured = capsys.readouterr()
    assert "fall 2024" in captured.out.lower()
    assert test_instructor["name"].lower() in captured.out.lower()

@pytest.mark.parametrize("date,expected", [
    (datetime.datetime(2000, 5, 1), "summer 2000"),
    (datetime.datetime(1999, 1, 1), "winter 1999"),
    (datetime.datetime(2024, 10, 15), "fall 2024")
])
def test_login_with_mocked_dates(monkeypatch, capsys, test_instructor, date, expected):
    mock_datetime = Mock()
    mock_datetime.now.return_value = date
    monkeypatch.setattr('instructor.datetime.datetime', mock_datetime)
    responses = iter([str(test_instructor["id"]), 'light', 'l', '', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()
    captured = capsys.readouterr()
    assert expected in captured.out.lower()

# --- COURSE SELECTION TESTS ---

def test_select_invalid_course(monkeypatch, capsys, test_instructor):
    responses = iter([str(test_instructor["id"]), 'light', test_instructor["invalid_course"], 'l', '', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()
    captured = capsys.readouterr()
    assert 'invalid course id' in captured.out.lower()

def test_select_valid_course(monkeypatch, capsys, test_instructor):
    responses = iter([str(test_instructor["id"]), 'light', test_instructor["courses"][0], 'x', '', 'l', '', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()
    captured = capsys.readouterr()
    assert "selected course" in captured.out.lower()

# --- GRADE & SORT TESTS ---

def test_check_empty_string(monkeypatch, capsys):
    responses = iter(['101', 'light', 'CS101', '1', 'n', '', '201', 'A', '', 'x', '', 'l', '', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    
    with pytest.raises(SystemExit) as exitInfo:
        main()
    captured = capsys.readouterr()
    assert "you must enter a student id" in captured.out.lower()

def test_add_course_invalid_instructor(monkeypatch, capsys):
    responses = iter(['45', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "invalid instructor id" in captured.out.lower()


def test_sort_courses(monkeypatch, test_instructor):

    # Setup
    gradebook = Gradebook()
    course_id = "CS101"
    gradebook.grades = {
        course_id: {
            201: {"grade": 88, "timestamp": None},
            202: {"grade": 72, "timestamp": None},
            203: {"grade": 95, "timestamp": None},
        }
    }

    # Mock input to simulate 'a' for ascending
    monkeypatch.setattr("builtins.input", lambda _: "a")

    # Run sort
    gradebook.sort_courses("a")

    # Extract sorted grades
    sorted_grades = list(gradebook.grades[course_id].items())
    grades_values = [entry["grade"] for _, entry in sorted_grades]

    # Check descending order (highest to lowest)
    assert grades_values == sorted(grades_values, reverse=True)

def test_grades_to_edit(monkeypatch):
    instructor = Instructor(101)  # Assigned to CS101
    gradebook = Gradebook()

    inputs = iter([
        "CS101", "201", "95",     # add_grade inputs
        "",                       # "Press enter to continue" after add
        "CS101", "201", "97", "y",# edit_grade inputs
        ""                        # "Press enter to continue" after edit
    ])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    # Add grade for CS101 student
    gradebook.add_grade(instructor, "CS101", 201, "95")

    # Edit grade (should be within 7 days)
    gradebook.edit_grade(instructor, "CS101", 201, "97")

    # View grades
    assert gradebook.grades_to_edit(instructor, "CS101") == True

def test_edit_invalid_id(monkeypatch, capsys, test_instructor):
    # Act & Arrange
    responses = iter([
        str(test_instructor["id"]), 'light', test_instructor["courses"][0],
        '1', 'n', '201', '99', '',
        '2', 'n', '202', '88', '',
        'x', '', 'l', '', 'q'
    ])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert "No grade exists for this student. Please use option 1 (Add Grade) to enter a new grade." in captured.out
