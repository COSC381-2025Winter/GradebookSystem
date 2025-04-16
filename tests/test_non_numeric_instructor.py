from main import main
import pytest

def test_login_with_invalid_id(monkeypatch, capsys):
    # Arrange
    responses = iter(['aaa', 'q'])  # invalid, then quit
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    #Act
    with pytest.raises(SystemExit):
        main()


    # Assert
    captured = capsys.readouterr()
    assert 'invalid instructor id' in captured.out.lower()