import os

def clear_screen():
    if os.getenv("DISABLE_CLEAR_SCREEN") == "1":
        return
    os.system('cls' if os.name == 'nt' else 'clear')
    return

# Add these missing print helpers
def print_error(message):
    print(f"\033[91mError: {message}\033[0m")

def print_success(message):
    print(f"\033[92m{message}\033[0m")

def print_warning(message):
    print(f"\033[93m{message}\033[0m")

def print_information(message):
    print(f"\033[94m{message}\033[0m")
