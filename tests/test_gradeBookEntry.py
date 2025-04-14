from main import main
import pytest

@pytest.fixture
def test_instructor():
    return {
        "id": 101,
        "name": "Dr. Smith",
        "courses": ["CS101", "CS111"],
    }

def test_empty_grade(monkeypatch, capsys, test_instructor):
    responses = iter([
        str(test_instructor["id"]),  # Instructor ID
        "light",                     # Theme
        "CS101",                     # Course
        "1",                         # Add grade
        "n",                         # Search by ID
        "201",                       # Student ID
        "",                          # Empty grade input
        "99",                        # Valid grade
        "", "x", "", "q"            # Continue, logout, quit
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "\tGrade cannot be empty" in captured.out
    assert "Grade added" in captured.out
    assert "201" in captured.out
