"""Logs information"""

import assistal.config as C

import os
import glob
import logging

logger = logging.getLogger(__name__)

log_methods = {
    'debug': logger.debug,
    'info': logger.info,
    'warning': logger.warning,
    'error': logger.error,
    'critical': logger.critical
}

class SizeLimitedFileHandler(logging.FileHandler):
    def __init__(self, filename, max_size_mb):
        super().__init__(filename, mode='a')
        self.max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes

    def emit(self, record):
        # Check file size
        if os.path.exists(self.baseFilename) and os.path.getsize(self.baseFilename) >= self.max_size_bytes:
            return
        
        super().emit(record)

def _create_log_dir_file():

    """Creates log directory and assings the current log's filename"""

    log_file_number = 1
    existed = True

    if not os.path.exists(C.LOG_PATH):
        os.mkdir(C.LOG_PATH)
        existed = False

    if existed:
        files_matching_today = glob.glob(os.path.join(C.LOG_PATH, "*" + C.LOG_FILE_NAME))
        total_files_matching_today = len(files_matching_today)

        # deletes files if they went over the limit
        if total_files_matching_today > C.MAX_LOGS_PER_DAY:
            for file_path in files_matching_today[:]:
                file_basename = os.path.basename(file_path)
                try:
                    number_part = int(file_basename.split('-')[0])
                    
                    if number_part > C.MAX_LOGS_PER_DAY:
                        os.remove(file_path)
                        files_matching_today.remove(file_path)

                except ValueError:
                    pass

            total_files_matching_today = C.MAX_LOGS_PER_DAY

        # moves existing logs so that the new one will be the first one
        if total_files_matching_today == C.MAX_LOGS_PER_DAY:

            files_sorted = sorted(files_matching_today, key=lambda file: int(os.path.basename(file).split('-')[0]))
            os.remove(files_sorted.pop(-1))

            for i in range(len(files_sorted) - 1, -1, -1):

                file_basename = os.path.basename(files_sorted[i])
                os.rename(files_sorted[i], os.path.join(C.LOG_PATH, str(i + 2) + file_basename[1:]))

        else:
            log_file_number = total_files_matching_today + 1

    FINAL_LOG_FILE = os.path.join(C.LOG_PATH, str(log_file_number) + "-" + C.LOG_FILE_NAME)

    return FINAL_LOG_FILE


def setup():

    FINAL_LOG_FILE = _create_log_dir_file()

    with open(FINAL_LOG_FILE, 'w') as log_file:
        log_file.write(f"[Assistal: process log]\n\n")

    handlers = []

    if C.VERBOSE:
        handlers.append(logging.StreamHandler())

    handlers.append(SizeLimitedFileHandler(FINAL_LOG_FILE, C.MAX_LOG_SIZE_BYTES))

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
