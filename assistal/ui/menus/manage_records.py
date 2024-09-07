from typing import Dict
from assistal.classes.Record import Record
from assistal.logger import log, plog
from assistal.xlsx import XLSX

import assistal.ui.commons as commons
import assistal.config as C

import time


def check_records():

    commons.print_text_ascii("Revisar Fichas")

def modify_records():

    doc = XLSX(C.RUNTIME_ASSISTANCE_FILE, Record.get_fields_listed())

    if not doc: return
    doc.write_on_change = True

    while True:
        commons.print_text_ascii("Modificar Fichas")

        doc.pretty_print()
        
        response: str = commons.show_form({"Que deseas hacer?": ["crear", "actualizar", "borrar", "regresar"]})[0]
        if response == "regresar":
            break

        if response == "crear":
            new_card_data = commons.show_form(Record.get_fields())

            final_card_data: Dict = Record.from_list(new_card_data)
            ok, level, message = \
                doc.create_entry(final_card_data), \
                "info", f"se logro crear al estudiante con identificacion {final_card_data["identificacion"]}"

            print()
            plog(level, f"{'not' if not ok else ''}{message}")

        elif response == "actualizar" or response == "borrar":
            student_id: int = commons.show_form({
                "Cual estudiante deseas gestionar (escribe la identificacion)?": (doc.has_entry, "la identificacion proporcionada no aparece en la tabla")
            })[0]

            ok = False
            message = f"se logro {response} a la identificacion {str(student_id)}"
            status = "info"
            if response == "borrar":
                ok = doc.delete_entry(student_id)
            else:
                new_card_data = commons.show_form(Record.get_fields(), allow_empty=True)

                final_card_data: Dict = Record.from_list(new_card_data)
                ok = doc.update_entry(student_id, final_card_data)

            if not ok:
                message = "no" + message
                status = "warning"

            print()
            plog(status, message)


        time.sleep(1)
        commons._clear_screen()


MENU_OPTIONS = {
    "📋  Revisar fichas": check_records,
    "📋  Modificar fichas": modify_records
}

def run():
    commons.show_menu(MENU_OPTIONS, "Fichas", show_exit=False)
