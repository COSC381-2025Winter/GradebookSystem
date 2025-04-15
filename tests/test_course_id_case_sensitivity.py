from main import main
import pytest, test_main
    
@pytest.fixture
def expected_output():
    return """
1. Add Grade
2. Edit Grade
3. View Grades
4. Sort Grades
x. Switch Course
"""

def test_Course_selection_with_lowercase(monkeypatch, capsys, expected_output):
    responses = iter([
        "101",     # Instructor ID
        "light",   # Theme
        "cs101",   # Course ID lowercase
        "x",       # Switch Course
        "",
        "l",       # Logout
        ""         # Confirm logout
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    main()
    captured = capsys.readouterr()
    assert expected_output.strip().lower() in captured.out.lower()


def test_Course_selection_with_uppercase(monkeypatch, capsys, expected_output):
    responses = iter([
        "101",     # Instructor ID
        "light",   # Theme
        "CS101",   # Course ID uppercase
        "x",       # Switch Course
        "",
        "l",       # Logout
        ""         # Confirm logout
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    main()
    captured = capsys.readouterr()
    assert expected_output.strip().lower() in captured.out.lower()


def test_Course_selection_with_mixed_input(monkeypatch, capsys, expected_output):
    responses = iter([
        "101",     # Instructor ID
        "light",   # Theme
        "Cs101",   # Course ID mixed-case
        "x",       # Switch Course
        "",
        "l",       # Logout
        ""         # Confirm logout
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    main()
    captured = capsys.readouterr()
    assert expected_output.strip().lower() in captured.out.lower()