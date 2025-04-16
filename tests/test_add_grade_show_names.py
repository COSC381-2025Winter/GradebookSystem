from main import main
import pytest

@pytest.fixture
def test_instructor():
    return {
        "id": 101,
        "name": "Dr. Smith",
        "courses": ["CS101", "CS111"],
    }

@pytest.fixture
def test_course():
    return {
        "id": "CS101",
        "name": "Intro to CS",
        "instructor_id": 101,
        "roster": [201]
    }

@pytest.fixture
def test_student():
    return {
        "id": "201",
        "name": "Alice"
    }

def test_show_names_when_adding_grade(monkeypatch, capsys, test_instructor, test_student, test_course):
    responses = iter([
    "101",       # Instructor ID
    "light",     # Theme
    "CS101",     # Course ID
    "1",         # Add Grade
    "n",         # Don't use helper search
    "201",       # Student ID
    "95",        # Grade
    "",          # Press enter after grade added
    "x",         # Switch course
    "",          # Press enter after switch
    "l",         # Logout
    "",          # ✅ Press enter after logout prompt (this was missing)
    'q'
])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(responses))
    monkeypatch.setattr("util.clear_screen", lambda: None)

    # Catch system exit at the end of main loop
    with pytest.raises(SystemExit) as exitInfo:
        main()

    captured = capsys.readouterr()

    # Check that the student name is shown when listing students
    assert test_student["name"].lower() in captured.out.lower()