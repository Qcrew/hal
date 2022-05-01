""" This module coordinates interactions between the log readers (backend) and the Notion client (frontend). This is the main script used to run Hal, built for invoking via CLI. """

import argparse
from datetime import datetime
from pathlib import Path
import time

from hal.dispatcher import LogDispatcher
from hal.logger import logger
from hal.reader import LogManager


@logger.catch
def run(path: Path, interval: int):
    """path: log folder path, interval: how often data will be read and posted by HAL"""

    try:
        old_date = datetime.now().strftime("%y-%m-%d")
        logger.debug(f"Entering HAL's main loop on '{old_date}'...")

        manager = LogManager(path / old_date)
        dispatcher = LogDispatcher()

        while True:
            new_date = datetime.now().strftime("%y-%m-%d")

            if old_date != new_date:  # account for Bluefors' log rotation
                subfolder = path / new_date
                if subfolder.exists():  # assume logfiles are created with the subfolder
                    logger.debug(f"Rerouting log manager to new {subfolder = }...")
                    manager = LogManager(subfolder)  # update log manager
                    old_date = new_date

            data = manager.data  # get data
            timestamp = datetime.now().strftime("%d %b %Y %I:%M:%S %p")
            logger.debug(f"Dispatching data with {timestamp = }...")
            dispatcher.post(timestamp, data)
            logger.debug(f"Sleeping for {interval}s till next update...")
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.debug("Exited after detecting keyboard interrupt!")


if __name__ == "__main__":
    """ """
    parser = argparse.ArgumentParser(description="Run HAL")
    parser.add_argument("path", type=Path, help="Path to the main logs folder")
    parser.add_argument("interval", type=int, help="How often data will be updated (s)")
    args = parser.parse_args()

    run(args.path, args.interval)
