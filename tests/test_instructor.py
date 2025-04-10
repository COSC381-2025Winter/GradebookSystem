import pytest
from instructor import Instructor
from color_theme import ColorTheme

import pytest
from instructor import Instructor

def test_default_theme():
    instructor = Instructor(instructor_id=101)
    assert instructor.get_theme() == "light"  # Default theme should be light

def test_set_dark_theme():
    instructor = Instructor(instructor_id=101)
    instructor.set_theme("dark")
    assert instructor.get_theme() == "dark"

def test_set_invalid_theme():
    instructor = Instructor(instructor_id=101)
    with pytest.raises(ValueError):
        instructor.set_theme("blue")  # Invalid theme should raise an error

def test_instructor_without_id():
    instructor = Instructor(instructor_id="nonexistent")
    assert instructor.name is None
    assert instructor.courses == []
    assert instructor.get_theme() == "light"  # Default theme should still be light

def test_instructor_courses():
    instructor = Instructor(instructor_id=101)
    expected_courses = {"CS101": "Intro to CS", "CS111": "Java Programming"}
    assert instructor.courses == expected_courses