import os
from assistal import config as C, fetcher
import assistal.ui.commons as commons
import assistal.xlsx as xlsx

def download_document():

    commons.print_text_ascii("Descargar Documento")
    fetcher.download_google_drive_file(C.GOOGLE_DRIVE_CARDS_DOCUMENT, C.RUNTIME_ASSISTANCE_FILE)
    
def manage_students():

    commons.print_text_ascii("Gestionar Estudiates")

def manage_cards():

    commons.print_text_ascii("Gestionar Fichas")

def generate_assistance():

    commons.print_text_ascii("Generar Asistencia")


MENU_OPTIONS = {
    "⬇️  Descargar documento con las fichas": download_document,
    "🧒  Gestionar estudiantes": manage_students,
    "💻  Gestionar las fichas": manage_cards,
    "📋  Generar asistencia": generate_assistance,
}

def run():
    commons.show_menu(MENU_OPTIONS, "ASSISTAL", use_small_banner=False, show_exit=True)
