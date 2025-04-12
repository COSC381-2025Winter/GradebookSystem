import datetime
from unittest.mock import patch, Mock
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


# Test quitting at Instructor ID input using 'q' or 'Q'
@pytest.mark.parametrize("quit_input", ['q', 'Q'])
def test_quit_on_instructor_input(monkeypatch, quit_input):
    monkeypatch.setattr('builtins.input', lambda _: quit_input)
    with pytest.raises(SystemExit):
        main()

# Test quitting at Course ID input using 'q' or 'Q'
@pytest.mark.parametrize("quit_input", ['q', 'Q'])
def test_quit_on_course_id_input(monkeypatch, quit_input):
    inputs = iter(['101', quit_input])  # Valid instructor ID, then quit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(SystemExit):
        main()


def test_check_empty_string(monkeypatch,capsys):
    #arrange
    responses = iter(['101','CS101','1','', '201','A','','x','','q'])
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
    # Mock datetime.datetime class in instructor module
    mock_datetime = Mock()
    mock_datetime.now.return_value = datetime.datetime(2024, 9, 15)
    monkeypatch.setattr('instructor.datetime.datetime', mock_datetime)
    expected_semester_year_string = "Fall 2024"

    responses = iter([str(test_instructor["id"]), 'q']) # Ensure ID is string
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()

    # Now we can assert the specific semester and year
    assert expected_semester_year_string.lower() in captured.out.lower()
    assert test_instructor["name"].lower() in captured.out.lower()
    assert test_instructor["courses"][0].lower() in captured.out.lower()
    assert test_instructor["courses"][1].lower() in captured.out.lower()
    assert exitInfo.value.code == None

    # Cleanup


# Test login with mocked date 5/1/2000
def test_login_with_mocked_date_2000(monkeypatch, capsys, test_instructor):
    # Arrange
    mock_datetime = Mock()
    mock_datetime.now.return_value = datetime.datetime(2000, 5, 1)
    monkeypatch.setattr('instructor.datetime.datetime', mock_datetime)
    expected_semester_year_string = "Summer 2000" # Corrected from Spring
    responses = iter([str(test_instructor["id"]), 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit):
        main()

    # Assert
    captured = capsys.readouterr()
    assert expected_semester_year_string.lower() in captured.out.lower()
    assert test_instructor["name"].lower() in captured.out.lower()


# Test login with mocked date 1/1/1999
def test_login_with_mocked_date_1999(monkeypatch, capsys, test_instructor):
    # Arrange
    mock_datetime = Mock()
    mock_datetime.now.return_value = datetime.datetime(1999, 1, 1)
    monkeypatch.setattr('instructor.datetime.datetime', mock_datetime)
    expected_semester_year_string = "Winter 1999"
    responses = iter([str(test_instructor["id"]), 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit):
        main()

    # Assert
    captured = capsys.readouterr()
    assert expected_semester_year_string.lower() in captured.out.lower()
    assert test_instructor["name"].lower() in captured.out.lower()


# Test login with mocked date 10/15/2024
def test_login_with_mocked_date_2024_oct(monkeypatch, capsys, test_instructor):
    # Arrange
    mock_datetime = Mock()
    mock_datetime.now.return_value = datetime.datetime(2024, 10, 15)
    monkeypatch.setattr('instructor.datetime.datetime', mock_datetime)
    expected_semester_year_string = "Fall 2024"
    responses = iter([str(test_instructor["id"]), 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit):
        main()

    # Assert
    captured = capsys.readouterr()
    assert expected_semester_year_string.lower() in captured.out.lower()
    assert test_instructor["name"].lower() in captured.out.lower()


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
    responses = iter([test_instructor["id"], test_instructor["courses"][0], 'x', '', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert "selected course" in captured.out.lower()
    assert f"{test_instructor['courses'][0]}".lower() in captured.out.lower()
    
    # Cleanup

def test_sort_courses(mocker, test_instructor):
    mock_input = mocker.patch('builtins.input', side_effect=[test_instructor["id"], test_instructor["courses"][0], '4', 'a', 'x','','q'])

    mock_sort_courses = mocker.patch('main.Gradebook.sort_courses')

    with pytest.raises(SystemExit):
        main()

    mock_sort_courses.assert_called_once_with('a')
