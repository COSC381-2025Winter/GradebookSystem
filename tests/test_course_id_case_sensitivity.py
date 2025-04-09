from main import main
import pytest, test_main


    
   
    
@pytest.fixture
def expected_output():
    x = """
1. add grade
2. edit grade
3. view grades
4. logout
"""

    return x

    
def test_Course_selection_with_lowercase(monkeypatch, capsys,expected_output):
# Act & Arrange
    responses = iter(["101","cs101", '4', ' ', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    
    with pytest.raises(SystemExit) as exitInfo:
        main()
        
    captured = capsys.readouterr()
    s = expected_output.lower()
   
  # Assert
    assert s in captured.out.lower()
    
def test_Course_selection_with_uppercase(monkeypatch, capsys,expected_output):
# Act & Arrange
    responses = iter(["101","CS101", '4', ' ', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    
    with pytest.raises(SystemExit) as exitInfo:
        main()
        
    captured = capsys.readouterr()
    s = expected_output.lower()
   
  # Assert
    assert s in captured.out.lower()
    
def test_Course_selection_with_mixed_input(monkeypatch, capsys,expected_output):
# Act & Arrange
    responses = iter(["101","Cs101", '4', ' ', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    
    with pytest.raises(SystemExit) as exitInfo:
        main()
        
    captured = capsys.readouterr()
    s = expected_output.lower()
   
  # Assert
    assert s in captured.out.lower()

    