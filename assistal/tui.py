def option_one():
    print("Option One Selected")

def option_two():
    print("Option Two Selected")

def option_three():
    print("Option Three Selected")

def exit_menu():
    print("Exiting menu.")
    exit()

MENU_OPTIONS = {
    "Descargar documento con las fichas": option_one,
    "Gestionar las fichas": option_two,
    "Generar asistencia": option_three,
}

def display_menu(menu):
    print("======== 📋 Assistal Menu 📋 ========\n")
    for index, key in enumerate(menu.keys(), start=1):
        print(f"{index}. {key}")
    print("0. Salir")

def _run_menu(menu):
    while True:
        display_menu(menu)
        print()
        choice = input("👉 ")
        
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
