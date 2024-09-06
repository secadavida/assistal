"""The main Assistal script"""

import assistal.logger as logger
import assistal.ui.cli as cli
import assistal.ui.tui as tui
import assistal.config as C

import os

def create_runtime():
     
    if not os.path.exists(C.RUNTIME_DIR):
        logger.log("info", "creando directorio del runtime")
        os.mkdir(C.RUNTIME_DIR)

    if not os.path.exists(C.RUNTIME_GROUPS_DIR):
        logger.log("info", "creando directorio para los grupos estudiantiles")
        os.mkdir(C.RUNTIME_GROUPS_DIR)

def main():

    cli.parse_arguments()

    logger.setup()
    logger.log("info", "inicializando Assistal")

    create_runtime()

    # NOTE: graceful exit, because any input() yields errors on KeyboardInterrupt
    try:
        tui.run()
    except KeyboardInterrupt:
        print()
        exit()
