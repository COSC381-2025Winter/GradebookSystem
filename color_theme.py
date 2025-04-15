from colorama import Fore, Back, Style
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
    if theme == "light":
        # Brighter text on dark background (now LIGHT MODE)
        set_theme_colors({
            "success": Fore.LIGHTGREEN_EX + Back.LIGHTWHITE_EX + Style.BRIGHT,
            "error": Fore.LIGHTRED_EX + Back.LIGHTWHITE_EX + Style.BRIGHT,
            "warning": Fore.LIGHTYELLOW_EX + Back.LIGHTWHITE_EX + Style.BRIGHT,
            "info": Fore.LIGHTCYAN_EX + Back.LIGHTWHITE_EX + Style.BRIGHT
        })
    elif theme == "dark":
        # Standard/neutral tone text (now DARK MODE)
        set_theme_colors({
            "success": Fore.GREEN + Back.BLACK,
            "error": Fore.RED + Back.BLACK,
            "warning": Fore.YELLOW + Back.BLACK,
            "info": Fore.BLUE + Back.BLACK
        })
    else:
        raise ValueError("Invalid theme. Choose 'light' or 'dark'.")

# 🔹 Module-level utility function for available themes
def list_available_themes():
    return ["light", "dark"]