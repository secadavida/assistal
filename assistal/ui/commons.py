import os
import time

import pyfiglet

FIGLET_BIG = pyfiglet.Figlet(font='slant')
FIGLET_MINI = pyfiglet.Figlet(font='mini')

def print_text_ascii(message: str, use_small_banner: bool = True) -> None:

    message = " ".join(message)

    text = FIGLET_MINI.renderText(message) if use_small_banner else FIGLET_BIG.renderText(message)
    
    print(text)

def _clear_screen():
    if os.name == 'nt': # windows
        os.system('cls')
    else:
        os.system('clear')

def display_menu(menu, banner_message: str, use_small_banner: bool = True, show_exit: bool = False):

    print_text_ascii(banner_message, use_small_banner)

    for index, key in enumerate(menu.keys(), start=1):
        print(f"{index}. {key}")
    print("0. ⬅️  " + ("Salir" if show_exit else "Regresar"))

def show_menu(menu, banner: str, use_small_banner: bool = True, show_exit: bool = False):

    while True:

        _clear_screen()
        display_menu(menu, banner, use_small_banner, show_exit)
        print()

        choice = input(" 👉  ")
        
        if choice == "0":
            if show_exit:
                exit()
            else:
                break
        
        try:
            choice_index = int(choice) - 1
            if choice_index in range(len(menu)):
                _clear_screen()
                list(menu.values())[choice_index]()
            else:
                print("Seleccion invalida: Por favor escribe uno de los numeros de la lista superior")

        except ValueError:
            print("Seleccion invaida: Por favor escribe un numero")

        time.sleep(1)

