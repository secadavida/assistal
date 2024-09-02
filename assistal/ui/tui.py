import assistal.ui.commons as commons

def download_document():

    print("download_document")
    pass
    
def manage_students():
    pass

def manage_cards():
    pass

def generate_assistance():
    pass


MENU_OPTIONS = {
    "⬇️  Descargar documento con las fichas": download_document,
    "🧒  Gestionar estudiantes": manage_students,
    "💻  Gestionar las fichas": manage_cards,
    "📋  Generar asistencia": generate_assistance,
}

def run():
    commons.show_menu(MENU_OPTIONS, "ASSISTAL", use_small_banner=False, show_exit=True)
