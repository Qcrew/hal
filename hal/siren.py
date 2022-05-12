""" Module that sends alerts to HAL's slack channel for alarming Param values """

from pathlib import Path
import time

import slack_sdk as slack
import slack_sdk.errors as slack_errors

from hal.logger import logger
from hal.param import Param

# a txt file must be at this path and contain two comma separated values in this format:
# <HAL's Slack token>,<#hal-alerts channel ID>
TOKENPATH = Path.cwd() / "slack_token.txt"


class Siren:
    """ """

    def __init__(self, remind_time: int = 600, retry_time: int = 30) -> None:
        """
        remind_time (int) in seconds, time to wait before sending alert again
        retry_time (int) in seconds, time to wait for before re-trying API call
        """
        self.remind_time = remind_time
        self.retry_time = retry_time

        token, self._channel_id = self._get_token()
        self._client = slack.WebClient(token=token)

        self.timestamps: dict[Param, float] = {}

        logger.debug(f"Siren ready to send alerts to Slack channel {self._channel_id}.")

    def _get_token(self) -> tuple[str, str]:
        """ """
        try:
            with TOKENPATH.open() as tokenfile:
                return tokenfile.read().split(",")
        except FileNotFoundError:
            message = (
                f"Please create a file named 'slack_token.txt' with the line '<HAL's"
                f"Slack token>,<#hal-alerts channel ID>' at {TOKENPATH.parent}."
            )
            logger.error(message)
            raise

    def alert(self, param: Param, value: str) -> None:
        """ """
        text = f"{param.name} {value = } is out of bounds {param.bounds}"

        timestamp = self.timestamps[param] if param in self.timestamps else 0
        # post only if more than self.remind_time has passed since last message
        if int(time.time() - timestamp) > self.remind_time:
            try:
                channel = self._channel_id
                result = self._client.chat_postMessage(channel=channel, text=text)
            except slack_errors.SlackApiError as error:
                logger.debug(f"Got {error = }, retrying after {self.retry_time}s...")
                time.sleep(self.retry_time)
                self.alert(param, value)
            else:
                if result.get("ok"):  # ensure no error response received
                    self.timestamps[param] = time.time()  # save for later check
                    logger.debug(f"Posted '{text = }' to slack!")
                else:
                    errorstring = result.get("error")
                    logger.debug(f"Didn't post '{text = }' due to {errorstring = }.")
        else:
            logger.debug(
                f"Didn't post '{text = }' as {self.remind_time}s have not elapsed "
                f"since the previous post."
            )
