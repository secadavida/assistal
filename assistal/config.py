"""Constants"""

import os
import tempfile
from datetime import datetime


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
_APP_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RUNTIME_DIR = _join(_APP_ROOT_DIR, "runtime")
RUNTIME_GROUPS_DIR = _join(RUNTIME_DIR, "groups")
RUNTIME_ASSISTANCE_DIR = _join(RUNTIME_DIR, "asistencia")

RUNTIME_RECORDS_FILE = _join(RUNTIME_DIR, "fichas.xlsx")
RUNTIME_ASSISTANCE_FILE = _join(RUNTIME_ASSISTANCE_DIR, "asistencia.xlsx")
GOOGLE_DRIVE_RECORDS_DOCUMENT = ""
