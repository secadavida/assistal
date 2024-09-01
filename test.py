import requests
from urllib.parse import urlparse, parse_qs

def extract_file_id_from_url(url):
    """
    Extracts the file ID from a Google Sheets URL.

    :param url: The Google Sheets URL.
    :return: The file ID extracted from the URL.
    """
    parsed_url = urlparse(url)
    # Extract file ID from the path or query parameters
    if 'd' in parse_qs(parsed_url.query):
        return parse_qs(parsed_url.query)['d'][0]
    else:
        # File ID is in the path segment
        path_segments = parsed_url.path.split('/')
        if len(path_segments) > 2:
            return path_segments[2]
    return None

def download_google_sheet_as_csv(url, destination):
    """
    Downloads a Google Sheets file as a CSV from Google Drive using the full URL.

    :param url: The Google Sheets URL.
    :param destination: The path where the downloaded CSV file will be saved.
    """
    # Extract the file ID from the URL
    file_id = extract_file_id_from_url(url)
    if not file_id:
        print("Invalid URL or unable to extract file ID.")
        return
    
    # Construct the URL to export the Google Sheets file as CSV
    export_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"

    # Send a request to get the file
    response = requests.get(export_url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the file to the destination
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded successfully to {destination}")
    else:
        print(f"Failed to download file: {response.status_code}")

# Example usage
sheet_url = 'https://docs.google.com/spreadsheets/d/1106U6_pnmgBm06o8Am0AHZNP4NYV2Eb9bakct6bec0o/edit?usp=drive_link'
destination = 'downloaded_file.csv'
download_google_sheet_as_csv(sheet_url, destination)
