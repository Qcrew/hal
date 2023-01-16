""" Entry point to run HAL """

import time

from hal.config import INTERVAL
from hal.dispatcher import Dispatcher
from hal.logger import logger
from hal.reader import Reader
from hal.siren import Siren


@logger.catch
def main():
    """
    HAL's main loop.

    Coordinates interaction between the reader, dispatcher, and the siren to read logfiles based on a user-specified config, post parameter values to Notion, and send alerts to a Slack channel.
    """
    logger.debug(f"Starting up HAL...")
    reader, dispatcher, siren = Reader(), Dispatcher(), Siren()

    try:
        while True:
            logger.debug("Reading and posting data...")
            data = reader.read()
            alerts = dispatcher.dispatch(data)
            if alerts:
                siren.warn(alerts)
            logger.debug(f"Sleeping for {INTERVAL}s till next update...")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        logger.debug("Stopped HAL due to keyboard interrupt.")


if __name__ == "__main__":
    main()
