"""Constants"""

import os
import tempfile
from datetime import datetime


_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _get_dir(*relative_path: str) -> str:

    return os.path.abspath(
        os.path.join(_BASE_DIR, *relative_path)
    )

_join = os.path.join


# meta
GENERATE_LOGS = True
VERBOSE = False

# runtime
LOG_FILE_NAME =  "assistal-" + datetime.now().strftime("%m-%d") + ".log"
LOG_PATH = _join(tempfile.gettempdir(), "assistal_logs")
MAX_LOGS_PER_DAY = 3
MAX_LOG_SIZE_BYTES = 5

# app logic
RUNTIME_DIR = _get_dir('..', 'data')
RUNTIME_GROUPS_DIR = _join(RUNTIME_DIR, "groups")
ESTUDIANTES_A = _join(RUNTIME_GROUPS_DIR, "A.xlsx")
CARDS_DOCUMENT = 'https://docs.google.com/spreadsheets/d/1106U6_pnmgBm06o8Am0AHZNP4NYV2Eb9bakct6bec0o/edit?usp=drive_link'
