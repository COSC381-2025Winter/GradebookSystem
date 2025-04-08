"""
This file is supposed to hold all the utility functions.
"""

import os

def clear_screen():
    if os.getenv("DISABLE_CLEAR_SCREEN") == "1":
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    return