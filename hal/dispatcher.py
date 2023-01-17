""" This module contains helpers that dispatch data via Notion's api. """

import time

from hal.client import Client
from hal.config import INTERVAL, PARAMS
from hal.logger import logger
from hal.param import Param


class Dispatcher:
    """ """

    SLEEP_TIME: float = 1.2  # time to wait between two dispatch requests

    def __init__(self) -> None:
        """ """
        self._interval: int = INTERVAL
        self._client: Client = Client()
        # for each param, save latest timestamp strings posted to Notion
        self._timestamps: dict[Param, str] = {param.name: "" for param in PARAMS}

    def dispatch(self, data: dict[Param, dict[str, str]]) -> dict[Param, str]:
        """
        data (dict) datadict as returned by the Reader
        return dict of alerts with key = Param object and value = param value
        """
        alerts = {}
        for param, values in data.items():
            last_updated_timestamp = self._timestamps[param]
            latest_timestamp = "" if not values else list(values)[-1]
            value = "N/A" if not values else param.parse(values[latest_timestamp])
            if latest_timestamp != last_updated_timestamp:
                if not param.validate(value):  # sound an alarm
                    logger.info(f"Got alert for {param.name} {value = }")
                    alerts[param] = value
                self._dispatch(param.name, value, latest_timestamp)
        return alerts

    def _dispatch(self, name: str, value: str, timestamp: str) -> None:
        """
        name (str) param name
        value (str) parsed value to post
        timestamp(str) timestamp associated with param value
        """
        success = self._client.post(name, value)
        if success:
            logger.info(f"Posted {name} = {value} as of {timestamp}.")
        else:
            logger.info(f"Error posting {name}={value}, retrying in {self._interval}s")
            time.sleep(self._interval)
            self._dispatch(name, value, timestamp)
        time.sleep(Dispatcher.SLEEP_TIME)
