import pytest
from instructor import Instructor

class TestInstructorTheme:

    def test_default_theme_is_light(self):
        instructor = Instructor(101)
        assert instructor.get_theme() == "light"

    def test_set_theme_to_dark(self):
        instructor = Instructor(101)
        instructor.set_theme("dark")
        assert instructor.get_theme() == "dark"

    def test_setting_invalid_theme_raises_error(self):
        instructor = Instructor(101)
        with pytest.raises(ValueError):
            instructor.set_theme("blue")

    def test_instructor_without_valid_id(self):
        instructor = Instructor(999)  # Assuming 999 is not in data.py
        # Adjust if Instructor class sets defaults like name="Unknown"
        assert instructor.name is None or instructor.name == "Unknown"
        assert instructor.courses == {}
        assert instructor.get_theme() == "light"

    def test_display_courses_outputs_expected_text(self, capsys):
        instructor = Instructor(101)
        instructor.display_courses()
        output = capsys.readouterr().out
        assert "CS101" in output or "CS111" in output or "Intro" in output or "Java" in output