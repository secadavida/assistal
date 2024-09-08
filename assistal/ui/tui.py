import assistal.config as C
import assistal.fetcher as fetcher
import assistal.ui.commons as commons
from assistal.xlsx import XLSX
from assistal.logger import plog
from assistal.classes.AssistanceEntry import AssistanceEntry
from assistal.classes.Record import Record

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

    records_doc = XLSX(C.RUNTIME_RECORDS_FILE, Record.get_fields_listed())

    if not records_doc: return
    records_doc.write_on_change = True

    assistance_doc = XLSX(C.RUNTIME_ASSISTANCE_FILE, AssistanceEntry.get_fields_listed())

    if not assistance_doc:
        plog("warning", "no se pudo leer el archivo de asistencia")

    assistance_doc.write_on_change = True

    for _, row in records_doc.df.iterrows():
        record = row.to_dict()

        new_entry = {
            "identificacion": record["identificacion"],
            "nombre_estudiante": record["nombre_estudiante"],
            "estado": "presente" if record["estado"] == "aceptado" else "ausente",
            "grado": record["grado"],
            "grupo": record["grupo"]
        }

        update_query = {
            "identificacion": record["identificacion"],
            "nombre_estudiante": record["nombre_estudiante"]
        }

        ok, level, message = True, "info", f"se pudo verificar la asistencia de {record["nombre_estudiante"]}"

        ok = assistance_doc.update_entry(update_query, new_entry)
        if not ok:
            ok = assistance_doc.create_entry(new_entry)

        if not ok:
            level, message = "warning", "no " + message

        plog(level, message)

    print()
    assistance_doc.pretty_print()

    commons.show_form({"Presiona <Enter> para regresar": str}, allow_empty=True)

MENU_OPTIONS = {
    "⬇️  Descargar documento con las fichas": download_document,
    "💻  Gestionar las fichas": manage_records,
    "🧒  Gestionar estudiantes": manage_students,
    "📋  Generar asistencia": generate_assistance,
}

def run():
    commons.show_menu(MENU_OPTIONS, "ASSISTAL", use_small_banner=False, show_exit=True)
