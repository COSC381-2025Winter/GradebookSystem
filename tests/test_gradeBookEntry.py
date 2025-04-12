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
    }

def test_empty_grade(monkeypatch, capsys, test_instructor):
    # Arrange
    responses = iter([
        test_instructor["id"],  # Instructor ID
        "light",                # Theme input
        "CS101",                # Course ID
        "1",                    # Add Grade
        "201",                  # Student ID
        "",                     # Empty grade (should trigger error)
        "99",                   # Valid fallback grade
        "",                     # Enter to continue
        "x",                    # Logout
        "",                     # Enter after logout
        "q"                     # Quit
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit):
        main()

    # Assert
    captured = capsys.readouterr()
    assert "\tGrade cannot be empty" in captured.out
    assert "Grade added for student 201" in captured.out