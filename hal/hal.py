""" This module coordinates interactions between the log readers (backend) and the Notion client (frontend). This is the main script used to run Hal. """

from datetime import datetime
from pathlib import Path
import time

from hal.dispatcher import LogDispatcher
from hal.logger import logger
from hal.reader import LogManager

LOG_FOLDER_PATH = Path("C:/Users/Qcrew4/Bluefors logs")
UPDATE_INTERVAL = 60  # in seconds


@logger.catch
def main():
    """ """
    try:
        old_date = datetime.now().strftime("%y-%m-%d")
        logger.debug(f"Entering HAL's main loop on '{old_date}'...")

        manager = LogManager(LOG_FOLDER_PATH / old_date)
        dispatcher = LogDispatcher()

        while True:
            new_date = datetime.now().strftime("%y-%m-%d")

            if old_date != new_date:  # account for Bluefors' log rotation
                subfolder = LOG_FOLDER_PATH / new_date
                if subfolder.exists():  # assume logfiles are created with the subfolder
                    logger.debug(f"Rerouting log manager to new {subfolder = }...")
                    manager = LogManager(subfolder)  # update log manager
                    old_date = new_date

            data = manager.data  # get data
            timestamp = datetime.now().strftime("%d %b %Y %I:%M:%S %p")
            logger.debug(f"Dispatching data with {timestamp = }...")
            dispatcher.post(timestamp, data)
            logger.debug(f"Sleeping for {UPDATE_INTERVAL}s till next update...")
            time.sleep(UPDATE_INTERVAL)
    except KeyboardInterrupt:
        logger.debug("Exited after detecting keyboard interrupt!")


if __name__ == "__main__":
    main()
