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
    # Arrange
    responses = iter([
        str(test_instructor["id"]),  # Instructor ID
        "light",                     # Theme
        "CS101",                     # Course
        "1",                         # Add Grade
        "n",                         # Don't search
        "201",                       # Student ID
        "",                          # ❌ Empty Grade (should trigger error)
        "99",                        # ✅ Valid Grade
        "",                          # Press enter after successful add
        "x",                         # Switch course
        "",                          # Enter after switch
        "l",                         # Logout
        "",                           # Enter after logout
        "q"
    ])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(responses))
    monkeypatch.setattr('main.clear_screen', lambda: None)

    # Act
    with pytest.raises(SystemExit) as exitInfo:
        main()
    captured = capsys.readouterr()

    # Assert
    assert "Grade cannot be empty" in captured.out
    assert "Grade added for student 201" in captured.out