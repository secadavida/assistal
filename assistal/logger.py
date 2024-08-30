"""Logs information"""

import assistal.config as C

import os
import logging

logger = logging.getLogger(__name__)

log_methods = {
    'debug': logger.debug,
    'info': logger.info,
    'warning': logger.warning,
    'error': logger.error,
    'critical': logger.critical
}



def setup():

    if os.path.exists(C.LOG_PATH):
        os.remove(C.LOG_PATH)

    with open(C.LOG_PATH, 'w') as log_file:
        log_file.write('[Assistal: process log]\n\n')

    handlers = []

    if C.VERBOSE:
        handlers.append(logging.StreamHandler())

    handlers.append(logging.FileHandler(C.LOG_PATH))

    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] (%(asctime)s): %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers = handlers
    )

def log(level: str, message: str) -> bool:

    log_method = log_methods.get(level.lower())

    if log_method:
        log_method(message)
        return True

    return False
