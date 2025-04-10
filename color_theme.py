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