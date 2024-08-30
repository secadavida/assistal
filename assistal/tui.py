import pyfiglet

FIGLET_BIG = pyfiglet.Figlet(font='slant')
FIGLET_MINI = pyfiglet.Figlet(font='mini')

def print_text_ascii(message: str, use_mini: bool = True) -> None:

    message = " ".join(message)

    text = FIGLET_MINI.renderText(message) if use_mini else FIGLET_BIG.renderText(message)
    
    print(text)


def download_document():
    print_text_ascii("Descargar documento")
    

def option_two():
    print("Option Two Selected")

def option_three():
    print("Option Three Selected")

def exit_menu():
    print("Exiting menu.")
    exit()

MENU_OPTIONS = {
    "⬇️  Descargar documento con las fichas": download_document,
    "💻  Gestionar las fichas": option_two,
    "📋  Generar asistencia": option_three,
}

def display_menu(menu):

    print_text_ascii("Assistal", False)

    for index, key in enumerate(menu.keys(), start=1):
        print(f"{index}. {key}")
    print("0. ⬅️  Salir")

def _run_menu(menu):

    while True:
        display_menu(menu)
        print()
        choice = input(" 👉  ")
        
        if choice == "0":
            exit_menu()
        
        try:
            choice_index = int(choice) - 1
            if choice_index in range(len(menu)):
                list(menu.values())[choice_index]()
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid selection. Please enter a number.")

def run_menu():
    _run_menu(MENU_OPTIONS)
