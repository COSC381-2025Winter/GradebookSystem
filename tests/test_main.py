import datetime
from unittest.mock import patch
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
@patch('main.datetime') # Patch datetime where it's used in the main module
def test_login_with_valid_id(mock_datetime, monkeypatch, capsys, test_instructor):
    # Arrange
    # Set a fixed date for the mock
    fixed_date = datetime.datetime(2024, 9, 15) # September 15, 2024
    mock_datetime.datetime.now.return_value = fixed_date

    responses = iter([str(test_instructor["id"]), 'q']) # Ensure ID is string
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()

    # Determine expected semester and year based on the fixed date
    current_month = fixed_date.month
    current_year = fixed_date.year
    if current_month in [12, 1, 2, 3, 4]:
        expected_semester = "Winter"
    elif current_month in [5, 6, 7, 8]:
        expected_semester = "Summer"
    else:  # Months 9, 10, 11
        expected_semester = "Fall"
    expected_semester_year_string = f"{expected_semester} {current_year}" # Fall 2024

    assert expected_semester_year_string.lower() in captured.out.lower() # Check for "Fall 2024"
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
