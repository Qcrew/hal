"""
Script to read sensor data from the ESP32 board and save it to a log file on disk. Currently, we are sensing cooling water flow only.
This script is meant to be always running in the background.
"""

from datetime import datetime
from pathlib import Path

from loguru import logger
import serial

PORT = "COM5"  # serial port to be read
BAUDRATE = 9600

# log file will be saved to LOGPATH / {yy-mm-dd} / {FILEPREFIX}{yy-mm-dd}.log
LOGPATH = Path("C:/Users/Qcrew4/Bluefors logs")
FILEPREFIX = "ESP32 "


def main():
    """ """
    board = serial.Serial(port=PORT, baudrate=BAUDRATE)
    logger.debug(f"Connected to {board = }.")
    old_date = get_datetime("%y-%m-%d")
    filepath = get_filepath(old_date)

    try:
        while True:
            # this readline() call returns only after a new line is available
            # hence, we retrieve the data first and then proceed to log it
            logger.debug("Waiting to receive sensor data...")
            data = board.readline()

            new_date = get_datetime("%y-%m-%d")
            if old_date != new_date:  # time to rotate log file
                filepath = get_filepath(new_date)
                logger.debug("Rotated logfile!")

            with filepath.open("a") as log:
                datestamp = get_datetime("%d-%m-%y")
                timestamp = get_datetime("%H:%M:%S")
                value = int(data.decode(encoding="utf-8", errors="ignore").strip())
                content = f"{datestamp},{timestamp},{value}\n"
                log.write(content)
                logger.debug(f"Received and wrote {content = } to logfile.")

    except KeyboardInterrupt:
        logger.debug("Exited after detecting keyboard interrupt!")


def get_filepath(date) -> Path:
    """ """
    subfolder = LOGPATH / date
    subfolder.mkdir(exist_ok=True)
    filepath = subfolder / f"{FILEPREFIX}{date}.log"
    logger.debug(f"Got {filepath = }.")
    return filepath


def get_datetime(fmt):
    """ """
    return datetime.now().strftime(fmt)


if __name__ == "__main__":
    """ """
    main()
