import pytest
from color_theme import apply_theme
from color_ui import (
    print_success,
    print_error,
    print_warning,
    print_information
)

# ANSI color codes for testing (from colorama.Fore)
from colorama import Fore

class TestColorThemeIntegration:

    def test_light_theme_success_color(self, capsys):
        apply_theme("light")
        print_success("Success")
        out = capsys.readouterr().out
        assert Fore.GREEN in out

    def test_dark_theme_success_color(self, capsys):
        apply_theme("dark")
        print_success("Success")
        out = capsys.readouterr().out
        assert Fore.LIGHTGREEN_EX in out

    def test_light_theme_error_color(self, capsys):
        apply_theme("light")
        print_error("Error")
        out = capsys.readouterr().out
        assert Fore.RED in out

    def test_dark_theme_info_color(self, capsys):
        apply_theme("dark")
        print_information("Info")
        out = capsys.readouterr().out
        assert Fore.LIGHTCYAN_EX in out