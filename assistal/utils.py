import os
import platform

def clear_screen():
    # Determine the operating system and issue the appropriate command
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
