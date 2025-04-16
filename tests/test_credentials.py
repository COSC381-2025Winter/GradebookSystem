# test_credentials.py

import pytest
from credentials import PASSWORDS
from data import INSTRUCTORS

@pytest.fixture
def valid_credentials():
    return {
        101: "csrocks",
        102: "javapro123",
        103: "algomaster",
        104: "softeng456"
    }

@pytest.fixture
def invalid_credentials():
    return {
        101: "wrongpass",
        102: "",
        103: "CSROCKS",  # wrong case
        999: "doesnotexist"
    }

def test_valid_passwords(valid_credentials):
    for instr_id, password in valid_credentials.items():
        assert PASSWORDS[instr_id] == password

def test_invalid_passwords(invalid_credentials):
    for instr_id, wrong_pw in invalid_credentials.items():
        assert PASSWORDS.get(instr_id) != wrong_pw

def test_instructor_ids_have_passwords():
    for instr_id in INSTRUCTORS:
        assert instr_id in PASSWORDS, f"Instructor {instr_id} has no password"

def test_invalid_instructor_id():
    assert PASSWORDS.get(999) is None
