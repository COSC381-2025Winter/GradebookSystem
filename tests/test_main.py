import datetime
from unittest.mock import patch, Mock
from main import main
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

# Test quitting at Instructor ID input using 'q' or 'Q'
@pytest.mark.parametrize("quit_input", ['q', 'Q'])
def test_quit_on_instructor_input(monkeypatch, quit_input):
    monkeypatch.setattr('builtins.input', lambda _: quit_input)
    with pytest.raises(SystemExit):
        main()

# Test quitting at Course ID input using 'q' or 'Q'
@pytest.mark.parametrize("quit_input", ['q', 'Q'])
def test_quit_on_course_id_input(monkeypatch, quit_input):
    inputs = iter(['101', 'light', quit_input]) # Add theme input
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(SystemExit):
        main()

@pytest.mark.parametrize("logout_input", ['exit', 'EXIT'])
def test_logout_on_course_id_input(monkeypatch, capsys, logout_input):
    inputs = iter([
        '101',         # Instructor ID
        'light',       # Theme selection
        logout_input,  # Course ID triggers 'exit'
        '',            # Press enter to continue
        'q'            # Instructor ID after main() restarts -> quit
    ])

    def fake_input(prompt):
        try:
            return next(inputs)
        except StopIteration:
            return 'q'

    monkeypatch.setattr(builtins, 'input', fake_input)

    # Patch the recursive main() call so it doesn't actually re-enter recursively
    with patch("main.main", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            main()

    # Verify that the logout message was printed
    captured = capsys.readouterr()
    assert "Logging out..." in captured.out

def test_check_empty_string(monkeypatch,capsys):
    #arrange
    responses = iter(['101', 'light','CS101','1','n', '', '201','A','','x','','q']) # Add theme and 'n' input
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "You must enter a student id!" in captured.out

def test_login_with_invalid_id(monkeypatch, capsys):
    responses = iter(['10', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert 'instructor id' in captured.out.lower()

def test_login_with_valid_id(monkeypatch, capsys, test_instructor):
    # Arrange
    # Mock datetime.datetime class in instructor module
    mock_datetime = Mock()
    mock_datetime.now.return_value = datetime.datetime(2024, 9, 15)
    monkeypatch.setattr('instructor.datetime.datetime', mock_datetime)
    expected_semester_year_string = "Fall 2024"

    responses = iter([str(test_instructor["id"]), 'light', 'q']) # Use monkeypatch mocking and add theme input
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()

    # Now we can assert the specific semester and year
    assert expected_semester_year_string.lower() in captured.out.lower()
    assert test_instructor["name"].lower() in captured.out.lower()
    assert test_instructor["courses"][0].lower() in captured.out.lower()
    assert test_instructor["courses"][1].lower() in captured.out.lower()

    # Cleanup is implicit with pytest fixtures


# Test login with mocked date 5/1/2000
def test_login_with_mocked_date_2000(monkeypatch, capsys, test_instructor):
    # Arrange
    mock_datetime = Mock()
    mock_datetime.now.return_value = datetime.datetime(2000, 5, 1)
    monkeypatch.setattr('instructor.datetime.datetime', mock_datetime)
    expected_semester_year_string = "Summer 2000" # Corrected from Spring
    responses = iter([str(test_instructor["id"]), 'light', 'q']) # Add theme input
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
    responses = iter([str(test_instructor["id"]), 'light', 'q']) # Add theme input
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
    responses = iter([str(test_instructor["id"]), 'light', 'q']) # Add theme input
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
    responses = iter([str(test_instructor["id"]), 'light', test_instructor["invalid_course"], 'q']) # Add theme input, ensure ID is string
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert 'invalid course id' in captured.out.lower()

def test_select_valid_course(monkeypatch, capsys, test_instructor):
    responses = iter([str(test_instructor["id"]), 'light', test_instructor["courses"][0], 'x', '', 'q']) # Add theme input, ensure ID is string
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "selected course" in captured.out.lower()
    assert test_instructor['courses'][0].lower() in captured.out.lower()

def test_add_course_invalid_instructor(monkeypatch, capsys):
    responses = iter(['45', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "Invalid Instructor ID" in captured.out
    assert "Traceback" not in captured.out

def test_sort_courses(mocker, test_instructor):
    mock_input = mocker.patch('builtins.input', side_effect=[
        str(test_instructor["id"]), 'light', test_instructor["courses"][0], # Ensure ID is string
        '4', 'a', 'x', '', 'q'
    ])
    mock_sort_courses = mocker.patch('main.Gradebook.sort_courses')

    with pytest.raises(SystemExit):
        main()

    mock_sort_courses.assert_called_once_with('a')

def test_grades_to_edit(monkeypatch, capsys, test_instructor):
    # Act & Arrange
    responses = iter([str(test_instructor["id"]), 'light', test_instructor["courses"][0], '1', 'n', '201', '99', '', '2', 'n', '201', '88', '', 'x', '', 'q']) # Ensure ID is string
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert "Alice (201): 99.0" in captured.out

def test_edit_invalid_id(monkeypatch, capsys, test_instructor):
    # Act & Arrange
    responses = iter([str(test_instructor["id"]), 'light', test_instructor["courses"][0], '1', 'n', '201', '99', '', '2', 'n', '202', '88', '', 'x', '', 'q']) # Ensure ID is string
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert "No grade exists for this student. Please use option 1 (Add Grade) to enter a new grade." in captured.out

  

