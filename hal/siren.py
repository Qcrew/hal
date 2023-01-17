""" Module that sends alerts to HAL's slack channel for alarming Param values """

import time

import slack_sdk as slack

from hal.config import FRIDGE_NAME, SLACK_TOKENPATH
from hal.logger import logger
from hal.param import Param


class Siren:
    """ """

    def __init__(self, remind_time: int = 600, retry_time: int = 30) -> None:
        """
        remind_time (int) in seconds, time to wait before sending alert again
        retry_time (int) in seconds, time to wait for before re-trying API call
        """
        self._remind_time = remind_time
        self._retry_time = retry_time
        with SLACK_TOKENPATH.open() as tokenfile:
            token, self._channel_id = tokenfile.read().split(",")
        self._client = slack.WebClient(token=token)
        self._log: dict[Param, float] = {}  # to record previous alert timestamp
        logger.info(f"Siren ready to send alerts to Slack channel {self._channel_id}.")

    def warn(self, param: Param, value: str) -> None:
        """ """
        timestamp = self._log[param] if param in self._log else 0
        text = f"{FRIDGE_NAME} {param.name} {value = } out of bounds {param.bounds}"
        channel = self._channel_id
        # post only if more than self.remind_time has passed since last message
        if int(time.time() - timestamp) > self._remind_time:
            result = self._client.chat_postMessage(channel=channel, text=text)
            if result.get("ok"):  # ensure no error response received
                self._log[param] = time.time()  # save for later check
                logger.info(f"Posted '{text = }' to slack!")
            else:
                errorstring = result.get("error")
                logger.debug(f"Didn't post '{text = }' due to {errorstring = }.")
