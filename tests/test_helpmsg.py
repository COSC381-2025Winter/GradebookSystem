from main import main
import pytest
import re

# 🔹 Improved ANSI stripper for reliable test output matching
def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def test_quitmsg(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: "q")
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "--- Gradebook System ---\nEnding program..." in captured.out

def test_quitmsg2(monkeypatch, capsys):
    responses = iter(['101', 'csrocks', 'dark', 'l', '', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Instructor found!\n" in captured.out
    assert "--- Gradebook System ---\nEnding program..." in captured.out

def test_validinfo(monkeypatch, capsys):
    responses = iter([
        '101', 'csrocks', 'dark', 'CS101', '1', 'n', '201', '50', '',  # Add grade
        '3', '',  # View grades
        'x', '', 'l', '', 'q'  # Exit
    ])
    monkeypatch.setattr('builtins.input', lambda *args: next(responses))
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    clean_output = strip_ansi(captured.out)
    assert "Valid Course ID!" in clean_output
    assert "Student found!" in clean_output
    assert "Grade added successfully!" in clean_output
    assert "Grades for Intro to CS (CS101):" in clean_output

def test_gradebookAscending(monkeypatch, capsys):
    responses = iter([
        '101', 'csrocks', 'dark', 'CS101',
        '1', 'n', '201', '60', '',       # Add grade
        '4', 'a',                        # Sort ascending
        '4', 'd',                        # Sort descending
        'x', '', 'l', '', 'q'
    ])
    monkeypatch.setattr('builtins.input', lambda *args: next(responses))
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    clean_output = strip_ansi(captured.out)
    assert "Grades sorted in ascending order!" in clean_output
    assert "Grades sorted in descending order!" in clean_output

def test_gradebookEdit(monkeypatch, capsys):
    responses = iter([
        '101', 'csrocks', 'dark',       # login
        'CS101',                        # course selection
        '1', 'n', '201', '60', '',      # add grade
        '2', 'n', '201', '70', 'y', '', '',  # edit grade
        'x', '', 'l', '', 'q'           # navigate back, logout, quit
    ])
    
    monkeypatch.setattr('builtins.input', lambda *args: next(responses, 'q'))
    
    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    clean_output = strip_ansi(captured.out)

    assert "Valid Course ID!" in clean_output
    assert "Grade updated for student 201: 70" in clean_output