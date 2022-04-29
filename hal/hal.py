""" This module coordinates interactions between the log readers (backend) and the Notion client (frontend). This is the main script used to run Hal. """

from datetime import datetime
from pathlib import Path
import time

from dispatcher import LogDispatcher
from logger import logger
from reader import LogManager

LOG_FOLDER_PATH = Path("C:/Users/Qcrew4/Bluefors logs")
UPDATE_INTERVAL = 150  # in seconds


@logger.catch
def main():
    """ """
    old_date = datetime.now().strftime("%y-%m-%d")
    logger.debug(f"Entering HAL's main loop on '{old_date}'...")

    manager = LogManager(LOG_FOLDER_PATH / old_date)
    dispatcher = LogDispatcher()

    while True:
        new_date = datetime.now().strftime("%y-%m-%d")

        if old_date != new_date:  # account for Bluefors' log rotation
            subfolder = LOG_FOLDER_PATH / new_date
            if subfolder.exists():  # assume logs are created together with subfolder
                logger.debug(f"Rerouting log manager to new {subfolder = }...")
                manager = LogManager(subfolder)  # update log manager
                old_date = new_date

        data = manager.data  # get data
        timestamp = datetime.now().strftime("%d %b %Y %I:%M:%S %p")
        logger.debug(f"Dispatched data with {timestamp = }.")
        dispatcher.post(timestamp, data)
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
