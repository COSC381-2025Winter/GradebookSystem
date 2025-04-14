from main import main
import pytest, test_main
    
@pytest.fixture
def expected_output():
    x = """
1. add grade
2. edit grade
3. view grades
4. sort grades
5. add student
x. logout
"""
    return x
  
def test_Course_selection_with_lowercase(monkeypatch, capsys, expected_output):
    responses = iter(["101", "light", "cs101", 'x', ' ', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    
    with pytest.raises(SystemExit):
        main()
        
    captured = capsys.readouterr()
    assert expected_output.lower() in captured.out.lower()
    
def test_Course_selection_with_uppercase(monkeypatch, capsys, expected_output):
    responses = iter(["101", "light", "CS101", 'x', ' ', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    
    with pytest.raises(SystemExit):
        main()
        
    captured = capsys.readouterr()
    assert expected_output.lower() in captured.out.lower()
    
def test_Course_selection_with_mixed_input(monkeypatch, capsys, expected_output):
    responses = iter(["101", "light", "Cs101", 'x', ' ', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    
    with pytest.raises(SystemExit):
        main()
        
    captured = capsys.readouterr()
    assert expected_output.lower() in captured.out.lower()
