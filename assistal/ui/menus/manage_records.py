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

    while True:
        commons.print_text_ascii("Revisar Fichas")

        doc.pretty_print(show_index=True)

        response: int = commons.show_form({"Cual ficha deseas marcar? (-1 para regresarse)": range(-1, len(doc.df)) })[0]
        if response == -1:
            return
        
        table_row = doc.get_row(response)

        ok, level, message = False, "warning", f"no se pudo actualizar la fila {response}"

        if table_row != None:
            updated_row = table_row.copy()
            current_estado = updated_row["estado"]

            # toggle the sate
            if not current_estado or current_estado != "revisado":
                updated_row["estado"] = "revisado"
            else:
                updated_row["estado"] = "rechazado"

            ok = doc.update_entry(table_row, updated_row)
            if ok:
                level, message = "info", f"se actualizo el estado de la fila {response} correctamente"

        plog(level, message)

        time.sleep(1)
        commons._clear_screen()

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

            new_record_data = commons.show_form(Record.get_fields("estado", "timestamp"))
            final_record_data: Dict[str, Any] = Record.from_list(new_record_data)

            ok, level, message = \
                doc.create_entry(final_record_data), \
                "info", f"se logro crear al estudiante con identificacion {final_record_data["identificacion"]}"

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
                new_record_data = commons.show_form(Record.get_fields("estado", "timestamp"), allow_empty=True)
                final_record_data: Dict[str, Any] = Record.from_list(new_record_data, allow_nones=True)

                ok = doc.update_entry(record_search_criteria, final_record_data)

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
