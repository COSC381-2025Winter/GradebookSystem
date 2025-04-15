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

# --- LOGOUT TEST ---

@pytest.mark.parametrize("logout_input", ['l', 'L'])
def test_logout_on_course_id_input(monkeypatch, capsys, logout_input):
    # Add extra inputs to avoid StopIteration
    inputs = iter(['101', 'light', logout_input, '', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

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
    responses = iter([str(test_instructor["id"]), 'light', 'l', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
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
    responses = iter([str(test_instructor["id"]), 'light', 'l', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    main()
    captured = capsys.readouterr()
    assert expected in captured.out.lower()

# --- COURSE SELECTION TESTS ---

def test_select_invalid_course(monkeypatch, capsys, test_instructor):
    responses = iter([str(test_instructor["id"]), 'light', test_instructor["invalid_course"], 'l', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    main()
    captured = capsys.readouterr()
    assert 'invalid course id' in captured.out.lower()

def test_select_valid_course(monkeypatch, capsys, test_instructor):
    responses = iter([str(test_instructor["id"]), 'light', test_instructor["courses"][0], 'x', '', 'l', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    main()
    captured = capsys.readouterr()
    assert "selected course" in captured.out.lower()

# --- GRADE & SORT TESTS ---

def test_check_empty_string(monkeypatch, capsys):
    responses = iter(['101', 'light', 'CS101', '1', 'n', '', '201', 'A', '', 'x', '', 'l', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
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


def test_sort_courses(mocker, test_instructor):
    mock_input = mocker.patch('builtins.input', side_effect=[
        str(test_instructor["id"]), 'light',
        test_instructor["courses"][0],
        '4', 'a',
        'x', '', 'l', '', 'q', ''
    ])
    mock_sort_courses = mocker.patch('main.Gradebook.sort_courses')
    
    main()
    
    mock_sort_courses.assert_any_call('a')  # or assert_called_once_with if you’re sure

def test_grades_to_edit(monkeypatch, capsys, test_instructor):
    responses = iter([
        str(test_instructor["id"]), 'light', test_instructor["courses"][0],
        '1', 'n', '201', '99', '',
        '2', 'n', '201', '88', '',
        'x', '', 'l', ''
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    main()
    captured = capsys.readouterr()
    assert "alice (201): 99.0" in captured.out.lower()

def test_edit_invalid_id(monkeypatch, capsys, test_instructor):
    responses = iter([
        str(test_instructor["id"]), 'light', test_instructor["courses"][0],
        '1', 'n', '201', '99', '',
        '2', 'n', '202', '88', '',
        'x', '', 'l', ''
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    main()
    captured = capsys.readouterr()
    assert "no existing grade found" in captured.out.lower()
