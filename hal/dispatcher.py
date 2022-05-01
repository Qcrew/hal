""" This module contains helpers that dispatch data via Notion's api. """

from pathlib import Path
import time

import notion_client as notion

from hal.logger import logger

# token.txt must be at this path and contain one value - HAL's Notion integration token
TOKENPATH = Path.cwd() / "token.txt"

# if we encounter an HTTP response error, wait before trying to post again
RETRY_TIME = 90  # seconds


class LogDispatcher:
    """ """

    def __init__(self) -> None:
        """ """
        self._client = notion.Client(auth=self._get_token())

        try:
            self._pageid = self._client.search()["results"][0]["id"]
            self._page_data = self._client.blocks.children.list(block_id=self._pageid)
        except notion.APIResponseError as error:
            if error.code == notion.APIErrorCode.Unauthorized:
                logger.error(f"Token found in {TOKENPATH} is invalid.")
            raise

        logger.debug(f"Log dispatcher ready to post to Notion page = {self._pageid}.")

    def _get_token(self) -> str:
        """ """
        try:
            with TOKENPATH.open() as tokenfile:
                return tokenfile.read()
        except FileNotFoundError:
            message = (
                f"Please create a file named 'token.txt' containing a single string "
                f"which is Hal's Notion integration token at {TOKENPATH.parent}."
            )
            logger.error(message)
            raise

    def post(self, timestamp: str, content: list[dict[str, str]]) -> None:
        """indexing follows block order set on Notion page"""
        # first, we update the dispatch timestamp
        count = 1  # 1st block is a divider, so we start our indexing count from 1
        self._post(text=f"Updated on {timestamp}", kind="heading_3", index=count)
        logger.debug(f"Updated {timestamp = }")

        # for this to work, the Notion page structure must be setup to match the content
        for datadict in content:
            count += 1  # account for the divider in between
            # Timestamp key is guaranteed to exist
            data_timestamp = f"Timestamp: {datadict.pop('Timestamp')}"
            for param, value in datadict.items():
                count += 1
                self._post(text=f"{param}: {value}", kind="heading_2", index=count)
                logger.debug(f"Updating {param}: {value}")
            count += 1
            self._post(text=data_timestamp, kind="paragraph", index=count)

        logger.debug(f"Posted data to Notion page with {timestamp = }.")

    def _post(self, text, kind, index):
        """internal method to post a no-frills simple block with the given text and kind (type) and block_id given by index"""
        block = {
            "type": kind,
            kind: {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "color": "default",
            },
        }
        block_id = self._page_data["results"][index]["id"]

        try:
            self._client.blocks.update(block_id=block_id, **block)
        except notion.errors.HTTPResponseError as error:
            if error.status == 502:
                # this error seems to be temporary and can be responded to by waiting
                # for REFRESH_INTERVAL before trying to post again
                message = f"Got 502 error, re-sending update after {RETRY_TIME}s..."
                logger.warning(message)
                time.sleep(RETRY_TIME)
                self._post(text, kind, index)
            else:
                raise
