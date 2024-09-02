"""The main Assistal script"""

import assistal.logger as logger
import assistal.ui.cli as cli
import assistal.ui.tui as tui


def main():

    cli.parse_arguments()

    logger.setup()
    logger.log("info", "inicializando Assistal")

    tui.run()
