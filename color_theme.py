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

# ---------- Global Theme Integration Helpers ----------

def apply_theme(theme_name):
    """
    Apply the selected theme globally by changing color_ui styles.
    """
    if theme_name == "dark":
        theme_colors = {
            "success": Fore.LIGHTGREEN_EX,
            "error": Fore.LIGHTRED_EX,
            "warning": Fore.LIGHTYELLOW_EX,
            "info": Fore.LIGHTCYAN_EX
        }
    else:  # light theme (default)
        theme_colors = {
            "success": Fore.GREEN,
            "error": Fore.RED,
            "warning": Fore.YELLOW,
            "info": Fore.BLUE
        }

    set_theme_colors(theme_colors)

def list_available_themes():
    return ["light", "dark"]