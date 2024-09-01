"""TUI"""

import assistal.fetcher as fetcher
import assistal.config as C

from assistal.classes.Estudiante import Estudiante
# from assistal.ui import commons
import assistal.ui.commons as commons
import assistal.menus.manage_students as _manage_students

import assistal.ui.utils as utils

def download_document():
    utils.print_text_ascii("Descargar documento")

    ok = fetcher.download_google_sheet(C.DOCUMENTO_CON_FICHAS, "datos.xlsx")
    
    if ok:
        print("se descargo el archivo correctamente")
    else:
        print("no se pudo descargar el archivo por falta de credenciales")
    
def manage_students():

    utils.print_text_ascii("Administrar estudiantes")

    Estudiante.crear_archivo(C.ESTUDIANTES_A) 
    _manage_students.run()

def manage_fichas():

    utils.print_text_ascii("Gestionar las fichas")

def generate_assistance():

    utils.print_text_ascii("Generar asistencia")

    name = input("Nombre: ")
    id = input("ID: ")

    student = Estudiante(name, id)

    student.agregar_a_excel(C.DOCUMENTO_CON_FICHAS)


MENU_OPTIONS = {
    "⬇️  Descargar documento con las fichas": download_document,
    "📋  Administrar estudiantes": manage_students,
    "💻  Gestionar las fichas": manage_fichas,
    "📋  Generar asistencia": generate_assistance,
}

def run():
    commons.run_menu(MENU_OPTIONS, "Assistal", small_banner=False, do_exit=True)
