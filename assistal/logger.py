"""Logs information"""

import assistal.config as C

import tempfile
import os
import logging

LOG_FILE_PATH = ""

logger = logging.getLogger(__name__)

log_methods = {
    'debug': logger.debug,
    'info': logger.info,
    'warning': logger.warning,
    'error': logger.error,
    'critical': logger.critical
}



def setup():
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Temporary directory path: {temp_dir}")

        LOG_FILE_PATH = os.path.join(temp_dir, C.LOG_FILE_NAME)

        # Check if the file exists
        if os.path.exists(LOG_FILE_PATH):
            os.remove(LOG_FILE_PATH)
        
        # Create a new file
        with open(LOG_FILE_PATH, 'w') as log_file:
            log_file.write('[Assistal: process log]')

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # logging.StreamHandler
            logging.FileHandler(LOG_FILE_PATH)
        ]
    )

def log(level: str, message: str) -> bool:

    log_method = log_methods.get(level.lower())

    if log_method:
        log_method(message)
        return True

    return False
