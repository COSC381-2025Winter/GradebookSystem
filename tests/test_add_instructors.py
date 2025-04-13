import pytest
import builtins
from main import main
import instructor

def test_add_instructor(monkeypatch, capsys):
    test_name = "Dr. Test"
    fake_id = 9999
    responses = iter([
        "0",           # Are you a new instructor?
        test_name,     # Enter instructor name
        str(fake_id),  # Enter instructor ID (mocked return)
        "q"            # Quit
    ])
    
    # Simulate input
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))

    # Temporarily mock add_instructor to avoid writing to data.py
    original_add = instructor.Instructor.add_instructor
    instructor.Instructor.add_instructor = staticmethod(lambda name: fake_id)

    try:
        with pytest.raises(SystemExit):
            main()
    finally:
        instructor.Instructor.add_instructor = original_add  # Restore after test

    captured = capsys.readouterr()
    assert f"Instructor '{test_name}' registered with ID {fake_id}" in captured.out
