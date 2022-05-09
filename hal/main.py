""" This module coordinates interactions between the log readers (backend) and the Notion client (frontend). This is the main script used to run Hal, built for invoking via CLI. """

import argparse
from pathlib import Path
import time

from hal.config import CONFIG
from hal.dispatcher import LogDispatcher
from hal.logger import logger
from hal.reader import LogReader


@logger.catch
def run(path: Path, interval: int):
    """path: log folder path, interval: how often data will be read and posted by HAL"""

    try:
        logger.debug(f"Entering HAL's main loop...")

        reader = LogReader(path, *CONFIG)
        dispatcher = LogDispatcher(interval)

        while True:
            data = reader.read()
            logger.debug(f"Dispatching data...")
            dispatcher.post(data)
            logger.debug(f"Sleeping for {interval}s till next update...")
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.debug("Exited after detecting keyboard interrupt!")


def main():
    """ method made for CLI usage """
    parser = argparse.ArgumentParser(description="Run HAL")
    parser.add_argument("path", type=Path, help="Path to the main logs folder")
    parser.add_argument("interval", type=int, help="How often data will be updated (s)")
    args = parser.parse_args()

    run(args.path, args.interval)


if __name__ == "__main__":
    """ """
    main()
