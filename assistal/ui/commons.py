import os
import sys
import time

import pyfiglet

FIGLET_BIG = pyfiglet.Figlet(font='slant')
FIGLET_MINI = pyfiglet.Figlet(font='mini')

from collections.abc import Callable
import time


def delete_all_lines_below_cursor():
    sys.stdout.write("\033[J")
    sys.stdout.flush()

def move_cursor_up(lines=1):
    sys.stdout.write(f"\033[{lines}A")
    sys.stdout.flush()

def move_cursor_down(lines=1):
    sys.stdout.write(f"\033[{lines}B")
    sys.stdout.flush()

def print_form_items(questions: dict[str, Callable], get_input = False):

    total_questions_left = len(questions)
    responses = []

    if get_input:
        move_cursor_up(total_questions_left)

    for key, value in questions.items():

        # construct displayable item
        item = f"\t+ {key}" 

        if isinstance(value, list):
            item += f" ({', '.join(value)}): "
        else:
            item += ": "

        if get_input:

            total_questions_left -= 1
            print(item, end = "")

            response = input()
            
            # get type assertion string
            type_ = value
            if isinstance(value, list):
                type_ = type(value[0])

            # try to convert the string to that type
            try:
                response = type_(response)
            except ValueError:
                return

            # omit all other questions if the current one couldn't be asserted
            if isinstance(value, list):
                if response not in value:
                    move_cursor_down(total_questions_left)
                    return

            responses.append(response)
        else:
            print(item)

    return responses


def show_form(questions):

    responses = []
    
    print()

    while True:
        print_form_items(questions)
        responses = print_form_items(questions, True)

        if responses is None:
            print("\n\tuna de las respuestas no tiene el formato requerido")
            time.sleep(1.5)

            move_cursor_up(len(questions) + 2)
            delete_all_lines_below_cursor()
        else:
            break

    return responses


def print_text_ascii(message: str, use_small_banner: bool = True) -> None:

    message = " ".join(message)

    text = FIGLET_MINI.renderText(message) if use_small_banner else FIGLET_BIG.renderText(message)
    
    print(text)

def _clear_screen():
    if os.name == 'nt': # windows
        os.system('cls') # type: ignore
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

