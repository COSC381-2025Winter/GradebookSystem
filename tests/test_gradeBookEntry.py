from main import main
import pytest
import re
import os

def remove_ansi(text):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

@pytest.fixture
def test_instructor():
    return {
        "id": 101,
        "name": "Dr. Smith",
        "courses": ["CS101", "CS111"],
    }

def test_empty_grade(monkeypatch, capsys, test_instructor, tmp_path):
    # Prepare clean grades.csv with header
    csv_path = tmp_path / "grades.csv"
    with open(csv_path, "w") as f:
        f.write("course_id,student_id,grade,timestamp\n")  # Header only

    # Patch the Gradebook constructor to use our temp file
    from gradebook import Gradebook
    monkeypatch.setattr("main.Gradebook", lambda: Gradebook(file_path=csv_path))

    # Simulated inputs
    responses = iter([
        test_instructor["id"],
        "light",
        "CS101",
        "1",     # Add Grade
        "n",     # Skip search
        "205",   # Unused student ID
        "",      # Empty grade
        "99",    # Valid grade
        "", "x", "", "q"
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    monkeypatch.setattr('main.clear_screen', lambda: None)

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    output = remove_ansi(captured.out)
    assert "\tGrade cannot be empty" in output
    assert "Grade added for student 205" in output
