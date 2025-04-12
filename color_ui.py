from colorama import Fore, Style

# Default color theme (light)
colors = {
    "success": Fore.GREEN,
    "error": Fore.RED,
    "warning": Fore.YELLOW,
    "info": Fore.BLUE
}

def set_theme_colors(theme_colors):
    global colors
    colors = theme_colors

def print_success(message):
    print(colors["success"] + message + Style.RESET_ALL)

def print_error(message):
    print(colors["error"] + message + Style.RESET_ALL)

def print_warning(message):
    print(colors["warning"] + message + Style.RESET_ALL)

def print_information(message):
    print(colors["info"] + message + Style.RESET_ALL)