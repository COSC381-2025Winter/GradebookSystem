from main import main
import pytest

# test program output after quitting (first input)
def test_quitmsg(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: "q")

    with pytest.raises(SystemExit) as exitInfo:
        main()

    captured = capsys.readouterr()
    assert "--- Gradebook System ---\nEnding program..." in captured.out

# test if instructor is valid and quit
def test_quitmsg2(monkeypatch, capsys):
    responses = iter(['101','dark','q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()

    captured = capsys.readouterr()
    assert "Instructor found!\n" in captured.out
    assert "--- Gradebook System ---\nEnding program..." in captured.out

# test if successfully found valid course ID, student ID, valid grade
def test_validinfo(monkeypatch, capsys):
    responses = iter(['101','dark','CS101','1','n','201','50.0', '','3', '', 'x','','q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    with pytest.raises(SystemExit) as exitInfo:
        main()

    captured = capsys.readouterr()
    assert "Valid Course ID!" in captured.out
    assert "Student found!" in captured.out
    assert "Grade added successfully!" in captured.out
    assert "\nGrades found!\n" in captured.out
    
# test if gradebook ascending/descending successfully prints
def test_gradebookAscending(monkeypatch, capsys):
    responses = iter(['101','dark','CS101',
                      '1','n','201','60.0', '',
                      '4', 'a', '4', 'd',
                      'x','','q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    
    with pytest.raises(SystemExit) as exitInfo:
        main()

    captured = capsys.readouterr()
    assert "Grades printed in ascending order!\n" in captured.out
    assert "Grades printed in descending order!\n" in captured.out
