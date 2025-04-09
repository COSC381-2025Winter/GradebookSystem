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

def test_check_empty_string(monkeypatch,capsys):
    #arrange
    responses = iter(['101','CS101','1','', '201','90','','4','','q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()

    #act
    captured = capsys.readouterr()

    #assert
    assert "You must enter a student id! " in captured.out


# the main function should ask for the user to log in at first
# test if the user enters an invalid digital id
def test_login_with_invalid_id(monkeypatch, capsys):
    # Arrange
    responses = iter(['10', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    

    # Act
    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert 'instructor id' in captured.out.lower()
    assert exitInfo.value.code == None

    # Cleanup

# test if the user enters a valid digital id
def test_login_with_valid_id(monkeypatch, capsys, test_instructor):
    # Arrange
    responses = iter([test_instructor["id"], 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert test_instructor["name"].lower() in captured.out.lower()
    assert test_instructor["courses"][0].lower() in captured.out.lower()
    assert test_instructor["courses"][1].lower() in captured.out.lower()
    assert exitInfo.value.code == None

    # Cleanup

# test select an invalid course
def test_select_invalid_course(monkeypatch, capsys, test_instructor):
    # Act & Arrange
    responses = iter([test_instructor["id"], test_instructor["invalid_course"], 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert 'invalid course id' in captured.out.lower()
    
    # Cleanup

# test select a valid course
def test_select_valid_course(monkeypatch, capsys, test_instructor):
    # Act & Arrange
    responses = iter([test_instructor["id"], test_instructor["courses"][0], '4', '', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert "selected course" in captured.out.lower()
    assert f"{test_instructor["courses"][0]}".lower() in captured.out.lower()
    
    # Cleanup

#test an invalid student ID
def test_invalid_studentID(monkeypatch, capsys, test_instructor):
    # Act & Arrange
    responses = iter([test_instructor["id"], test_instructor["courses"][0], '1', '1', '4', '', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert "Invalid Student ID." in captured.out
    
    # Cleanup