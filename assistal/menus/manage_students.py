import assistal.ui.utils as utils

from assistal.classes.Estudiante import Estudiante
import assistal.ui.commons as commons

def create_student():
    utils.print_text_ascii("Crear un estudiante")

def edit_student():
    utils.print_text_ascii("Editar un estudiante")

def delete_student():
    utils.print_text_ascii("Borrar un estudiante")

MENU_OPTIONS = {
    "Crear un estudiante": create_student,
    "Editar un estudiante": edit_student,
    "Borrar un estudiante": delete_student,
}

def run():
    commons.run_menu(MENU_OPTIONS, "Manage Students")
