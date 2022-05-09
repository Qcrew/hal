""" This module contains helpers that dispatch data via Notion's api. """

from datetime import datetime
from pathlib import Path
import time

import httpx
import numpy as np
import notion_client as notion

from hal.logger import logger
from hal.param import Param

# token.txt must be at this path and contain one value - HAL's Notion integration token
TOKENPATH = Path.cwd() / "token.txt"


class LogDispatcher:
    """ """

    def __init__(self, interval: int) -> None:
        """
        interval (int) time to wait for before posting again if we encounter an HTTP response error
        """
        self.interval = interval
        self._client = notion.Client(auth=self._get_token())

        try:
            self._page_id = self._client.search()["results"][0]["id"]
            self._page_data = self._client.blocks.children.list(block_id=self._page_id)
        except notion.APIResponseError as error:
            if error.code == notion.APIErrorCode.Unauthorized:
                logger.error(f"Token found in {TOKENPATH} is invalid.")
            raise

        # get block id of block containing main timestamp
        self._timestamp_id = self._page_data["results"][0]["id"]

        # get block id and content of the table displaying the data
        self._table_id = self._page_data["results"][1]["id"]
        self._table_data = self._client.blocks.children.list(block_id=self._table_id)

        logger.debug(f"Log dispatcher ready to post to Notion page = {self._page_id}.")

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

    def post(self, data: dict[Param, tuple[np.ndarray, np.ndarray]]) -> None:
        """ """
        self._post_timestamp()  # first, we update the main timestamp

        # NOTE the Notion page structure must be setup to match the data structure
        for index, (param, (timestamps, values)) in enumerate(data.items()):
            if timestamps is None or values is None:
                self._post_table_row("N/A", param.name, "N/A", index)
            else:
                timestamp = timestamps[-1][:-3]  # ignore ss, only extract hh:mm
                value = param.parse(values[-1])
                self._post_table_row(timestamp, param.name, value, index)

        logger.debug(f"Posted data to Notion page.")

    def _post_timestamp(self) -> None:
        """ """
        timestamp = f"As of {datetime.now().strftime('%d %b %Y %I:%M:%S %p')}"
        block = {
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": timestamp}}],
                "color": "default",
            },
        }
        self._post(self._timestamp_id, **block)
        logger.debug(f"Updated {timestamp = }.")

    def _post_table_row(self, timestamp, name, value, index) -> None:
        """ """
        block = {
            "type": "table_row",
            "table_row": {
                "cells": [
                    [{"type": "text", "text": {"content": timestamp}}],
                    [{"type": "text", "text": {"content": name}}],
                    [{"type": "text", "text": {"content": value}}],
                ]
            }
        }
        block_id = self._table_data["results"][index]["id"]
        self._post(block_id, **block)
        logger.debug(f"Posted [{timestamp}, {name}, {value}] to row {index + 1}.")

    def _post(self, block_id, **block):
        """ """
        try:
            self._client.blocks.update(block_id=block_id, **block)
        except notion.errors.HTTPResponseError as error:
            # this error class is temporary so we respond by waiting and re-trying
            message = f"Got {error = }, re-sending data after {self.interval}s..."
            logger.warning(message)
            time.sleep(self.interval)
            self._post(block_id, **block)
        except httpx.ConnectError as error:
            # this error class requires client re-initialization
            message = (
                f"Got {error = }, re-starting client and re-sending data after"
                f"{self.interval}s..."
            )
            logger.warning(message)
            self._client(auth=self._get_token())
            time.sleep(self.interval)
            self._post(block_id, **block)
