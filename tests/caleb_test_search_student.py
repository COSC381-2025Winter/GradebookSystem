import pytest 
from main import main 

@pytest.fixture
def test_instructor():
    # Uses instructor from data.py
    # 101, Dr. Smith
    # "CS101": {"name": "Intro to CS", "instructor_id": 101},
    # "CS111": {"name": "Java Programming", "instructor_id": 101},
    return {
        "id": 101,
        "name": "Dr. Smith",
        "courses": ["CS101", "CS111"],
        "invalid_course": "CSabc"
    }

@pytest.fixture
def test_course():
    # use course from data.py
    # "CS101": {"name": "Intro to CS", "instructor_id": 101}
    # "CS101": [201, 202, 203, 204, 205, 206]
    return {
        "id": "CS101",
        "name": "Intro to CS",
        "instructor_id": 101,
        "roster": [201, 202, 203, 204, 205, 206]
    }

@pytest.fixture
def test_student():
    # uses a student from data.py
    # 201: "Alice"
    return {
        "id": [201, 203],
        "name": ["Alice", "Charlie"]
    }

# test if matching student is displayed after searching for one specific student using their id
def test_matching_student_displayed(monkeypatch, capsys, test_instructor, test_student, test_course):
    # Arrange
    responses = iter([test_instructor["id"], test_course["id"], "4", str(test_student["id"][0]), "\n", "back", "5", "\n", "q"])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert test_student["name"][0] in captured.out
    assert str(test_student["id"][0]) in captured.out

# test if matching students are displayed after searching for letter "c" that may be apart of multiple students; names
def test_display_students_containing_letter_match(monkeypatch, capsys, test_instructor, test_student, test_course):
    # Arrange
    responses = iter([test_instructor["id"], test_course["id"], "4", "c", "\n", "back", "5", "\n", "q"])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert test_student["name"][0] in captured.out
    assert str(test_student["id"][0]) in captured.out
    assert test_student["name"][1] in captured.out
    assert str(test_student["id"][1]) in captured.out

# test if no matching students found displays message
def test_no_matching_students(monkeypatch, capsys, test_instructor, test_student, test_course):
    # Arrange
    responses = iter([test_instructor["id"], test_course["id"], "4", "zxy", "\n", "back", "5", "\n", "q"])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert "No matching students found." in captured.out