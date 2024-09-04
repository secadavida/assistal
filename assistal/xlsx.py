from assistal.logger import log, plog
from assistal.ui import commons

import pandas as pd
import os


def create_file(column_headers, destination_file) -> bool:
    df = pd.DataFrame(columns=column_headers)
    
    if os.path.isfile(destination_file):
        plog("warning", f"ya hay un archivo presente en '{destination_file}'")
        responses = commons.show_form({"Deseas reemplazarlo?": ["si", "no"]})
        if responses[0] == "no":
            plog("info", f"el archivo en '{destination_file}' fue dejado intacto")
            return False

        df.to_excel(destination_file, index=False, engine='openpyxl')

    return True
