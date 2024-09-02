"""Fetch files from Google Drive"""

from assistal.logger import log

import requests
import re

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

def download_google_sheet(url: str, destination: str) -> bool:

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

    # send a request to get the file
    response = requests.get(export_url, stream=True)

    # check if the request was successful
    if response.status_code == 200:
        # Write the file to the destination
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        log("info", f"se descargo el archivo: {url}")
        return True

    log("error", f"no se pudo descargar el archivo: {url}. Estatus: {str(response.status_code)}")
    return False
