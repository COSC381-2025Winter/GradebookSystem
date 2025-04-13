from main import main
import pytest

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
    #use course from data.py
    #"CS101": {"name": "Intro to CS", "instructor_id": 101}
    #"CS101": [201, 202, 203, 204, 205, 206]
    return {
        "id": "CS101",
        "name": "Intro to CS",
        "instructor_id": 101,
        "color_theme": "light",
        "roster": [201, 202, 203, 204, 205, 206]
    }

@pytest.fixture
def test_student():
    #uses a student from data.py
    #201: "Alice"
    return {
        "id": 201,
        "name": "Alice"
    }


#test if name is being displayed after student id number when adding student
def test_show_names_when_adding_grade(monkeypatch, capsys, test_instructor, test_student, test_course):
    #Arrange
    responses = iter([test_instructor["id"], 
                    "light",
                    test_course["id"],
                    "1", "n", test_student["id"], "A", "\n", "x", "\n", "q"])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    #Act
    with pytest.raises(SystemExit) as exitInfo:
        main()
    
    #Assert
    captured = capsys.readouterr()
    assert test_student["name"].lower() in captured.out.lower()