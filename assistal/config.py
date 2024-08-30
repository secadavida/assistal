"""Constants"""

import os
import tempfile
from datetime import datetime


_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _get_dir(*relative_path) -> str:

    return os.path.abspath(
        os.path.join(_BASE_DIR, *relative_path)
    )

def _join(*paths) -> str:
    
    return os.path.join(*paths)


# meta
GENERATE_LOGS = True
VERBOSE = False
LOG_FILE_NAME = "assistal-" + datetime.now().strftime("%m-%d") + ".log"
LOG_PATH = os.path.join(tempfile.gettempdir(), LOG_FILE_NAME)

# app logic
DATA_DIR = _get_dir('..', 'data')
DATA_GROUPS_DIR = _join(DATA_DIR, "groups")
