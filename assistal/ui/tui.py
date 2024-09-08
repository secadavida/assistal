import assistal.config as C
import assistal.fetcher as fetcher
import assistal.ui.commons as commons

import assistal.ui.menus.manage_records as manage_records_


def download_document():

    commons.print_text_ascii("Descargar Documento")
    fetcher.download_google_drive_file(C.GOOGLE_DRIVE_RECORDS_DOCUMENT, C.RUNTIME_RECORDS_FILE, merge_criteria=["timestamp", "identificacion"])
    
def manage_students():

    commons.print_text_ascii("Gestionar Estudiates")

def manage_records():

    commons.print_text_ascii("Gestionar Fichas")
    manage_records_.run()

def generate_assistance():

    commons.print_text_ascii("Generar Asistencia")


MENU_OPTIONS = {
    "⬇️  Descargar documento con las fichas": download_document,
    "💻  Gestionar las fichas": manage_records,
    "🧒  Gestionar estudiantes": manage_students,
    "📋  Generar asistencia": generate_assistance,
}

def run():
    commons.show_menu(MENU_OPTIONS, "ASSISTAL", use_small_banner=False, show_exit=True)
