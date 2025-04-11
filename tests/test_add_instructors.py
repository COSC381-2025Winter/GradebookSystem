# test_instructor_utils.py
import pytest
from instructor import Instructor, add_instructor
from data import INSTRUCTORS

@pytest.fixture(autouse=True)
def reset_instructors():
    """
    Resets the INSTRUCTORS dictionary before and after each test.
    """
    original = INSTRUCTORS.copy()
    yield
    INSTRUCTORS.clear()
    INSTRUCTORS.update(original)

def test_add_instructor_adds_to_dict():
    name = "Dr. Pytest"
    new_id = add_instructor(name)
    assert new_id in INSTRUCTORS
    assert INSTRUCTORS[new_id] == name

def test_add_instructor_creates_unique_id():
    initial_ids = set(INSTRUCTORS.keys())
    name = "Dr. New"
    new_id = add_instructor(name)
    assert new_id not in initial_ids
    assert isinstance(new_id, int)

def test_add_multiple_instructors():
    name1 = "Dr. A"
    name2 = "Dr. B"
    id1 = add_instructor(name1)
    id2 = add_instructor(name2)
    assert id1 != id2
    assert INSTRUCTORS[id1] == name1
    assert INSTRUCTORS[id2] == name2
