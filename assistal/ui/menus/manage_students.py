
MENU_OPTIONS = {
    "📋  Administrar grupos": generate_assistance,
    "📋  Crear estudiante": generate_assistance,
    "📋  Editar estudiante": generate_assistance,
    "📋  Borrar estudiante": generate_assistance,
}

def run():
    commons.show_menu(MENU_OPTIONS, "ASSISTAL", use_small_banner=False, show_exit=True)
