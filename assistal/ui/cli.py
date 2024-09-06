import assistal.config as C

import argparse

def parse_arguments() -> None:

    parser = argparse.ArgumentParser(description="CLI parser for Assistal")

    parser.add_argument("-v", "--verbose", action='store_true', help="mostrar los logs en pantalla")
    parser.add_argument("-n", "--no-logs", action='store_true', help="no generar logs (los cuales se guardan el directorio temporal del sistema operativo)")
    parser.add_argument("-f", "--fichas", type=str, default="", help="URL de Google Drive con el archivo donde se guardan las fichas")

    args = parser.parse_args()

    C.VERBOSE = args.verbose
    C.GENERATE_LOGS = False if args.no_logs else True

    if args.fichas != "":
        C.GOOGLE_DRIVE_RECORDS_DOCUMENT = args.fichas
