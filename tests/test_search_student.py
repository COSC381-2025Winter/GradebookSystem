import pytest
from main import main

@pytest.fixture
def test_instructor():
    return {
        "id": "101",
        "name": "Dr. Smith",
        "courses": ["CS101", "CS111"],
        "invalid_course": "CSabc"
    }

@pytest.fixture
def test_course():
    return {
        "id": "CS101",
        "name": "Intro to CS",
        "instructor_id": "101",
        "roster": ["201", "202", "203", "204", "205", "206"]
    }

@pytest.fixture
def test_student():
    return {
        "id": ["201", "203"],
        "name": ["Alice", "Charlie"]
    }

def test_matching_student_displayed(monkeypatch, capsys, test_instructor, test_student, test_course):
    responses = iter([
        test_instructor["id"], 'csrocks', 'light', test_course["id"],
        '1', 'y', test_student["id"][0], '', 'back',
        test_student["id"][0], '85', '', 'x', '', 'l', '', 'q'
    ])
    monkeypatch.setattr('builtins.input', lambda *args: next(responses))
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert test_student["name"][0] in captured.out
    assert test_student["id"][0] in captured.out

def test_display_students_containing_letter_match(monkeypatch, capsys, test_instructor, test_student, test_course):
    responses = iter([
        test_instructor["id"], 'csrocks', 'light', test_course["id"],
        '1', 'y', 'c', '', 'back',
        test_student["id"][1], '68', '', 'x', '', 'l', '', 'q'
    ])
    monkeypatch.setattr('builtins.input', lambda *args: next(responses))
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert test_student["name"][0] in captured.out
    assert test_student["id"][0] in captured.out
    assert test_student["name"][1] in captured.out
    assert test_student["id"][1] in captured.out

def test_no_matching_students(monkeypatch, capsys, test_instructor, test_student, test_course):
    responses = iter([
        test_instructor["id"], 'csrocks', 'light', test_course["id"],
        '1', 'y', 'zxy', '', 'back',
        test_student["id"][0], '99', '', 'x', '', 'l', '', 'q'
    ])
    monkeypatch.setattr('builtins.input', lambda *args: next(responses))
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "No matching students found." in captured.out