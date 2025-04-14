from main import main
import pytest

@pytest.fixture
def test_instructor():
    # Uses instructor from data.py
    return {
        "id": 101,
        "name": "Dr. Smith",
        "courses": ["CS101", "CS111"],
        "invalid_course": "CSabc"
    }

@pytest.fixture
def test_course():
    # Uses course from data.py
    return {
        "id": "CS101",
        "name": "Intro to CS",
        "instructor_id": 101,
        "color_theme": "light",
        "roster": [201, 202, 203, 204, 205, 206]
    }

@pytest.fixture
def test_student():
    # Uses student from data.py
    return {
        "id": 201,
        "name": "Alice"
    }

# Test if student name is displayed after entering student ID when adding grade
def test_show_names_when_adding_grade(monkeypatch, capsys, test_instructor, test_student, test_course):
    # Arrange
    responses = iter([
        str(test_instructor["id"]),     # Instructor ID as string
        test_course["color_theme"],     # Theme
        test_course["id"],              # Course ID
        "1",                            # Option to add grade
        "n",                            # Do not search students by name
        str(test_student["id"]),        # Student ID as string (important!)
        "A",                            # Grade (invalid, will fail & prompt again)
        "90",                           # Valid numeric grade
        "",                             # Press enter to continue
        "x",                            # Logout
        "",                             # Press enter after logout
        "q"                             # Quit system
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit):
        main()

    # Assert
    captured = capsys.readouterr()
    assert test_student["name"].lower() in captured.out.lower()
