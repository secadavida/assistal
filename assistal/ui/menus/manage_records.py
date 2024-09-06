from assistal.classes.Record import Record
import assistal.ui.commons as commons
import assistal.config as C
from assistal.xlsx import XLSX

def check_records():

    commons.print_text_ascii("Revisar Fichas")
    # display_records()

def modify_records():

    doc = XLSX(C.RUNTIME_ASSISTANCE_FILE, Record.get_fields_listed())

    if not doc: return

    while True:
        commons.print_text_ascii("Modificar Fichas")

        doc.pretty_print()
        
        response: str = commons.show_form({"Que deseas hacer?": ["crear", "actualizar", "borrar", "regresar"]})[0]
        if response == "regresar":
            break

        if response == "crear":
            new_student_data = commons.show_form(Record.get_fields())
        elif response == "actualizar" or response == "borrar":
            student_id: int = commons.show_form({
                "Cual estudiante deseas gestionar (escribe la identificacion)?": (doc.read_entry, "la identificacion proporcionada no aparece en la tabla")
            })[0]

        commons._clear_screen()


MENU_OPTIONS = {
    "📋  Revisar fichas": check_records,
    "📋  Modificar fichas": modify_records
}

def run():
    commons.show_menu(MENU_OPTIONS, "Fichas", show_exit=False)
