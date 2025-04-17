import pytest
from io import StringIO
import sys
from main import main  # Adjust if your main script has a different name or structure


def run_test_with_inputs(inputs, expected_output, monkeypatch, capsys):
    responses = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    
    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr().out

    # Remove ANSI escape sequences (color codes)
    import re
    cleaned_output = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', captured)

    # Clean up whitespace and compare in lowercase
    assert expected_output.lower().strip() in cleaned_output.lower().strip()


@pytest.mark.parametrize("input_sequence", [
    ["101", "light", "cs101", 'x', ' ', 'q'],   # lowercase
    ["101", "light", "CS101", 'x', ' ', 'q'],   # uppercase
    ["101", "light", "Cs101", 'x', ' ', 'q'],   # mixed case
])
def test_Course_selection_variants(input_sequence, monkeypatch, capsys):
    expected_output = (
        "1. add grade\n"
        "2. edit grade\n"
        "3. view grades\n"
        "4. sort grades\n"
        "5. delete grades\n"
        "x. logout"
    )
    run_test_with_inputs(input_sequence, expected_output, monkeypatch, capsys)

