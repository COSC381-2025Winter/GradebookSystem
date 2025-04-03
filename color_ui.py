from colorama import Fore, Back, Style

def print_success(message):
    print(Fore.GREEN + message + Style.RESET_ALL)

def print_error(message):
    print(Fore.RED + message + Style.RESET_ALL)

def print_warning(message):
    print(Fore.YELLOW + message + Style.RESET_ALL)

def print_information(message):
    print(Fore.BLUE + message + Style.RESET_ALL)