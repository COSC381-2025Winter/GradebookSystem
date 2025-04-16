import pytest
import builtins
import getpass
from main import main
import instructor

def test_add_instructor(monkeypatch, capsys):
    test_name = "Dr. Test"
    fake_id = 9999
    fake_password = "0000"  # getpass returns a string

    # Define responses for input calls:
    # 1. "0" – for selecting new instructor.
    # 2. test_name – to provide the instructor's name.
    # 3. "" – simulating pressing enter after seeing the success message.
    # 4. "q" – at the top-level prompt, to quit.
    responses = iter([
        "0",          # Selecting new instructor
        test_name,    # Instructor's name input
        "",           # After successful registration, "Press Enter to continue..."
        "q"           # When prompted again at the top-level, quit the application
    ])

    # Monkeypatch built-in input to use our responses.
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(responses))
    # Monkeypatch getpass.getpass to return our fake password.
    monkeypatch.setattr(getpass, "getpass", lambda prompt="": fake_password)

    # Temporarily mock add_instructor to avoid writing to data.py.
    original_add = instructor.Instructor.add_instructor
    instructor.Instructor.add_instructor = staticmethod(lambda name, password: fake_id)

    try:
        with pytest.raises(SystemExit):
            main()
    finally:
        # Restore the original add_instructor method
        instructor.Instructor.add_instructor = original_add

    captured = capsys.readouterr()
    assert f"Instructor '{test_name}' registered with ID {fake_id}" in captured.out
