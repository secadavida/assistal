"""Fetch files from Google Drive
    
Caveats:
 - It can only handle URLs that "Anyone can access", other than that will require
    the use of credentials.json from Google's API from the file's owner
 - Only supports the file formats specified under $FILE_FORMATS
"""

import time
from assistal.logger import log, plog
from assistal.ui import commons

from tqdm import tqdm
import requests
import re
import os


FILE_FORMATS = {
    "spreadsheets": "xlsx",
    "document": "docx"
}

def extract_file_properties(url):
    """
    Extracts the file ID from a Google Sheets URL.

    :param url: The Google Drive file's URL.
    :return: The file type (e.g. 'spreadsheets') and the file ID extracted from the URL.
    """

    matched_type = re.search(r"docs\.google\.com/([^/]+)/d/", url)
    matched_id = re.search(r'/d/([a-zA-Z0-9_-]+)', url)

    properties = []

    properties.append(matched_type.group(1) if matched_type else None)
    properties.append(matched_id.group(1) if matched_id else None)

    return *properties,

def download_google_drive_file(url: str, destination: str) -> bool:

    file_type, file_id = extract_file_properties(url)

    if not file_id:
        log("error", "no se pudo extraer el ID del archivo en Google Drive")
        return False

    if not file_type:
        log("error", "no se pudo extraer el tipo del archivo en Google Drive")
        return False
    
    export_format = FILE_FORMATS[file_type] or None
    
    if not export_format:
        log("error", "el archivo que se esta intentando descargar no es soportado por el programa")
        return False
    
    # construct the URL to export the Google Sheets file as CSV
    export_url = f"https://docs.google.com/{file_type}/d/{file_id}/export?format={export_format}"

    log("info", "revisando la disponibilidad del archivo")

    # send a GET request for the file
    response = requests.get(export_url, stream=True)

    # check if the request was successful
    if response.status_code == 200:
        
        log("info", f"el archivo {url} se encuentra disponible para descargar")

        if os.path.isfile(destination):
            plog("warning", f"ya hay un archivo presente en '{destination}'")
            responses = commons.show_form({"Deseas reemplazarlo?": ["si", "no"]})
            if responses[0] == "no":
                plog("info", f"el archivo en '{destination}' fue dejado intacto")
                return False

        plog("info", f"se reemplazara el archivo en '{destination}'")

        # Total file size (in bytes) - You may need to get this from response.headers['Content-Length']
        total_size = int(response.headers.get('Content-Length', 0))

        # Create a tqdm progress bar
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024)

        # Write the content to a file
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))

        # Close the progress bar
        progress_bar.close()
        
        plog("info", f"se descargo el archivo: {url}")
        time.sleep(2)
        return True

    plog("error", f"no se pudo descargar el archivo: {url}. Estatus: {str(response.status_code)}")
    return False
