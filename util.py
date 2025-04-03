"""
This file is supposed to hold all the utility functions.
"""

import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')