import assistal.config as C

import argparse

def parse_arguments() -> None:

    parser = argparse.ArgumentParser(description="CLI parser for Assistal")

    parser.add_argument("-v", "--verbose", action='store_true', help='Increase output verbosity')
    parser.add_argument("-n", "--no-logs", action='store_true', help='Increase output verbosity')

    args = parser.parse_args()

    C.VERBOSE = args.verbose
    C.GENERATE_LOGS = False if args.no_logs else True
