import os
import sys
import time
from pandas.core.common import inspect
import pyfiglet

from typing import Callable, Any, Dict, List, Optional, Tuple, Union
import time

FIGLET_BIG = pyfiglet.Figlet(font='slant')
FIGLET_MINI = pyfiglet.Figlet(font='mini')


def delete_all_lines_below_cursor():
    sys.stdout.write("\033[J")
    sys.stdout.flush()

def move_cursor_up(lines=1):
    sys.stdout.write(f"\033[{lines}A")
    sys.stdout.flush()

def move_cursor_down(lines=1):
    if lines == 0: return
    sys.stdout.write(f"\033[{lines}B")
    sys.stdout.flush()


# example
# FORM = {
#     "question 1?": None,
#     "question 2?": ["opt1", "opt2"],
#     "question 3?": (assert_function, "on_fail message")
#     "question 4?": int
#
# }
def print_form_items(questions: dict[str, Callable], total_questions: int, get_input = False, allow_empty: bool = False):

    responses = []

    if get_input:
        move_cursor_up(total_questions)

    for key, value in questions.items():

        # construct displayable item
        item = f"\t+ {key}" 

        if isinstance(value, list):
            item += f" ({', '.join(value)}): "
        elif isinstance(value, range):
            item += f" ({value[0]}-{value[-1]}): "
        else:
            item += ": "

        if value is None:
            if get_input:
                responses.append(None)
            continue

        if get_input:
            
            total_questions -= 1
            print(item, end = "")

            response = input()
            if response == "":
                if not allow_empty:
                    move_cursor_down(total_questions)
                    return responses, f"la respuesta al campo '{key}' no puede estar vacia"
                else:
                    responses.append(None)
                    continue

            if isinstance(value, tuple):
                parameters = inspect.signature(value[0]).parameters
                first_param_type = list(parameters.values())[0].annotation

                # try to convert the string to the type of the function's first parameter
                try:
                    response = first_param_type(response)
                except ValueError:
                    move_cursor_down(total_questions)
                    return responses, f"la respuesta al campo '{key}' no tiene es del tipo apropiado"

                if not value[0](response):
                    move_cursor_down(total_questions)
                    return responses, value[1]

            elif isinstance(value, list):
                type_: Callable[[Any], Any] = type(value[0])

                # try to convert the string to that type
                try:
                    response = type_(response)
                except ValueError:
                    move_cursor_down(total_questions)
                    return responses, f"La respuesta al campo '{key}' no es de tipo {type_.__name__}"

                if response not in value:
                    move_cursor_down(total_questions)
                    return responses, f"La respuesta al campo '{key}' no es ninguna de {value}"

            elif isinstance(value, range):
                
                # try to convert the string to int
                try:
                    response = int(response)
                except ValueError:
                    move_cursor_down(total_questions)
                    return responses, f"La respuesta al campo '{key}' no es de tipo int"

                if response not in value:
                    move_cursor_down(total_questions)
                    return responses, f"La respuesta al campo '{key}' no esta en el rango ({value[0]}-{value[-1]})"

            elif value != None: # is a casting func
                type_: Callable[[Any], Any] = value
                try:
                    response = value(response)
                except ValueError:
                    move_cursor_down(total_questions)
                    return responses, f"La respuesta al campo '{key}' no es de tipo {type_.__name__}"

            responses.append(response)
        else:
            print(item)

    return responses, None

def show_form(questions: Dict, cumulative_callback: Optional[Tuple[Callable[[Dict[str, Any]], Any], str]] = None, allow_empty: bool = False) -> List[Any]:

    responses = []
    total_questions = sum(1 for _, v in questions.items() if v is not None)
    if total_questions == 0:
        return responses

    print()

    while True:
        print_form_items(questions, total_questions)
        responses, retval = print_form_items(questions, total_questions, get_input=True, allow_empty=allow_empty)

        if cumulative_callback:
            responses_dict = {key: value for key, value in zip(questions.keys(), responses)}
            if not cumulative_callback[0](responses_dict):
                responses, retval = [], cumulative_callback[1]

        if retval:
            print(f"\n\terror: {retval}")
            time.sleep(1.5)

            move_cursor_up(total_questions + 2)
            delete_all_lines_below_cursor()
        else:
            break

    return responses

def show_form_get_dict(questions: Dict, cumulative_callback: Optional[Tuple[Callable[[Dict[str, Any]], Any], str]] = None, allow_empty: bool = False) -> Dict[str, Any]:
    responses = show_form(questions, cumulative_callback, allow_empty)

    return {key: value for key, value in zip(questions.keys(), responses)}

def print_text_ascii(message: str, use_small_banner: bool = True) -> None:

    message = " ".join(message)

    text = FIGLET_MINI.renderText(message) if use_small_banner else FIGLET_BIG.renderText(message)
    
    print(text)

def _clear_screen():
    if os.name == 'nt': # windows
        os.system('cls') # type: ignore
    else:
        os.system('clear')

def display_fields(menu, banner_message: str, use_small_banner: bool = True, show_exit: bool = False, print_vals: bool = True):

    print_text_ascii(banner_message, use_small_banner)

    if print_vals:
        for key, value in menu.items():
            print(f"\t+ {key}: {value}")
    else:
        for index, key in enumerate(menu.keys(), start=1):
            print(f"{index}. {key}")

def show_menu(menu, banner: str, use_small_banner: bool = True, show_exit: bool = False):

    while True:

        _clear_screen()
        display_fields(menu, banner, use_small_banner, show_exit, print_vals=False)
        print("0. ⬅️  " + ("Salir" if show_exit else "Regresar"))
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

