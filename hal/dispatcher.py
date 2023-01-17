""" This module contains helpers that dispatch data via Notion's api. """

import time

from hal.client import Client
from hal.config import INTERVAL, DELAY, PARAMS
from hal.logger import logger
from hal.param import Param


class Dispatcher:
    """ """

    def __init__(self) -> None:
        """ """
        self._interval: int = INTERVAL
        self._client: Client = Client()
        # for each param, save latest timestamp strings posted to Notion
        self._timestamps: dict[Param, str] = {param.name: "" for param in PARAMS}

    def dispatch(self, data: dict[Param, dict[str, str]], siren) -> dict[Param, str]:
        """
        data (dict) datadict as returned by the Reader
        siren (Siren) to send warnings if any Params are out of bounds
        return dict of alerts with key = Param object and value = param value
        """
        for param, values in data.items():
            last_updated_timestamp = self._timestamps[param.name]
            latest_timestamp = "N/A" if not values else list(values)[-1]
            if latest_timestamp == "N/A":
                self._dispatch(param, "N/A", latest_timestamp)
            elif latest_timestamp != last_updated_timestamp:
                value = param.parse(values[latest_timestamp])
                if not param.validate(value):  # sound an alarm
                    print(f"SENDING ALARM FOR {param}, {value}")
                    siren.warn(param, value)
                self._dispatch(param, value, latest_timestamp)
                self._timestamps[param.name] = latest_timestamp

    def _dispatch(self, param: Param, value: str, timestamp: str) -> None:
        """
        name (Param) param object
        value (str) parsed value to post
        timestamp(str) timestamp associated with param value
        """
        success = self._client.post(param, value)
        if success:
            logger.info(f"Posted {param.name} = {value} as of {timestamp}.")
        else:
            logger.info(f"Error posting {param.name} = {value}, retrying...")
            time.sleep(self._interval)
            self._dispatch(param, value, timestamp)
        time.sleep(DELAY)
