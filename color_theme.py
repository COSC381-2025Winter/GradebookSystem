from colorama import Fore
from color_ui import set_theme_colors

class ColorTheme:
    def __init__(self, theme="light"):
        """
        Initializes a ColorTheme object with a default theme.
        Args:
            theme (str): The color theme, either "light" or "dark".
        """
        self.set_theme(theme)

    def set_theme(self, theme):
        """
        Set the theme to either 'light' or 'dark'.
        Args:
            theme (str): The theme to set ('light' or 'dark').
        """
        if theme not in ["light", "dark"]:
            raise ValueError("Invalid theme. Choose 'light' or 'dark'.")
        self.theme = theme

    def get_theme(self):
        """
        Return the current theme.
        """
        return self.theme

# 🔹 Module-level utility function for applying the theme globally
def apply_theme(theme):
    """
    Apply the color theme globally using set_theme_colors.
    """
    if theme == "light":
        set_theme_colors({
            "success": Fore.GREEN,
            "error": Fore.RED,
            "warning": Fore.YELLOW,
            "info": Fore.BLUE
        })
    elif theme == "dark":
        set_theme_colors({
            "success": Fore.LIGHTGREEN_EX,
            "error": Fore.LIGHTRED_EX,
            "warning": Fore.LIGHTYELLOW_EX,
            "info": Fore.CYAN
        })
    else:
        raise ValueError("Invalid theme. Choose 'light' or 'dark'.")

# 🔹 Module-level utility function for available themes
def list_available_themes():
    return ["light", "dark"]