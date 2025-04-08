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
    responses = iter([(test_instructor["id"]), "CS101", "1", "201", " ", "b", "", "4", "", "q"])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))

    # Act
    with pytest.raises(SystemExit) as exitInfo:
        main()

    # Assert
    captured = capsys.readouterr()
    assert "\tInvalid grade entered" in captured.out

