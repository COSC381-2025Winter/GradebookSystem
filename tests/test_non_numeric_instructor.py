from main import main
import pytest

# the main function should ask for the user to log in at first
# test if the user enters an invalid non-numeric id 
def test_login_with_invalid_id(monkeypatch, capsys):
    # Arrange
    responses = iter(['aaa', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    
    
    # Act
    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert 'instructor id' in captured.out.lower()
    assert exitInfo.value.code == None