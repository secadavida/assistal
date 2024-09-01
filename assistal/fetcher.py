"""Fetch files from Google Drive"""

import requests
import re

def extract_file_id_from_url(url):
    """
    Extracts the file ID from a Google Sheets URL.

    :param url: The Google Sheets URL.
    :return: The file ID extracted from the URL.
    """
    # Regular expression to find file ID in Google Sheets URL
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None

def download_google_sheet(url, destination):
    # Extract the file ID from the URL
    file_id = extract_file_id_from_url(url)
    if not file_id:
        print("Invalid URL or unable to extract file ID.")
        return
    
    # Construct the URL to export the Google Sheets file as CSV
    export_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"

    # Send a request to get the file
    response = requests.get(export_url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the file to the destination
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return True
    return False
