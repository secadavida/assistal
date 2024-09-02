import assistal.config as C

import argparse

def parse_arguments() -> None:

    parser = argparse.ArgumentParser(description="CLI parser for Assistal")

    parser.add_argument("-v", "--verbose", action='store_true', help="Increase output verbosity")
    parser.add_argument("-n", "--no-logs", action='store_true', help="Do not generate log files")
    parser.add_argument("-f", "--fichas", type=str, default="", help="Google Drive url for the cards file")

    args = parser.parse_args()

    C.VERBOSE = args.verbose
    C.GENERATE_LOGS = False if args.no_logs else True

    if args.fichas != "":
        C.CARDS_DOCUMENT = args.fichas
