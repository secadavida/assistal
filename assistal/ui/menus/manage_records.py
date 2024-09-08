from typing import Any, Dict, List
from assistal.classes.Record import Record
from assistal.logger import log, plog
from assistal.xlsx import XLSX

import assistal.ui.commons as commons
import assistal.config as C

import time


def check_records():

    doc = XLSX(C.RUNTIME_ASSISTANCE_FILE, Record.get_fields_listed())


    if not doc: return
    doc.write_on_change = True

    # while True:
    #
    # commons.print_text_ascii("Revisar Fichas")

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

            new_card_data = commons.show_form(Record.get_fields("estado", "timestamp"))
            final_card_data: Dict[str, Any] = Record.from_list(new_card_data)

            ok, level, message = \
                doc.create_entry(final_card_data), \
                "info", f"se logro crear al estudiante con identificacion {final_card_data["identificacion"]}"

            print()
            plog(level, f"{'not' if not ok else ''}{message}")

        elif response == "actualizar" or response == "borrar":

            print("Cual ficha deseas gestionar?")
            record_search_criteria = commons.show_form_get_dict({
                "identificacion": int,
                "timestamp": str
            }, cumulative_callback=(doc.query, "no se encontro ninguna fila que cumpliera con esos campos"))

            ok, level, message = False, \
                "info", f"se logro {response} la ficha con timestamp \
                    {str(record_search_criteria['timestamp'])} e identificacion {str(record_search_criteria['identificacion'])}"

            if response == "borrar":
                ok = doc.delete_entry(record_search_criteria)
            else:
                new_card_data = commons.show_form(Record.get_fields("estado", "timestamp"), allow_empty=True)
                final_card_data: Dict[str, Any] = Record.from_list(new_card_data, allow_nones=True)

                ok = doc.update_entry(record_search_criteria, final_card_data)

            if not ok:
                message = "no" + message
                level = "warning"

            print()
            plog(level, message)


        time.sleep(1)
        commons._clear_screen()


MENU_OPTIONS = {
    "📋  Revisar fichas": check_records,
    "📋  Modificar fichas": modify_records
}

def run():
    commons.show_menu(MENU_OPTIONS, "Fichas", show_exit=False)
