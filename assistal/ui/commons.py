import assistal.ui.utils as utils
import assistal.utils as _utils
import time

def display_menu(menu, banner: str, small_banner: bool = True, show_exit: bool = False):

    utils.print_text_ascii(banner, small_banner)

    for index, key in enumerate(menu.keys(), start=1):
        print(f"{index}. {key}")
    print("0. ⬅️  " + ("Salir" if show_exit else "Regresar"))

def run_menu(menu, banner: str, small_banner: bool = True, do_exit: bool = False):

    while True:

        _utils.clear_screen()

        display_menu(menu, banner, small_banner, do_exit)
        print()
        choice = input(" 👉  ")
        
        if choice == "0":
            if do_exit:
                exit()
            else:
                break
        
        try:
            choice_index = int(choice) - 1
            if choice_index in range(len(menu)):
                list(menu.values())[choice_index]()
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid selection. Please enter a number.")

