""" This module contains helpers that dispatch data via Notion's api. """

from pathlib import Path

import notion_client as notion

from logger import logger

# token.txt must be present at this path with two comma separated values: token, url
TOKENPATH = Path(__file__).resolve().parent / "token.txt"


class LogDispatcher:
    """ """

    def __init__(self) -> None:
        """ """
        with TOKENPATH.open() as tokenfile:
            token, url = tokenfile.read().split(",")
        self._client = notion.Client(auth=token)
        self._pageid = notion.helpers.get_id(url)
        self._page_data = self._client.blocks.children.list(block_id=self._pageid)

        logger.debug(f"Log dispatcher ready to post to Notion page = {url}.")

    def post(self, timestamp: str, content: dict[str, dict[str, str]]) -> None:
        """indexing follows block order set on Notion page"""
        # TODO the count updating is a little loose, need to devise a better strategy
        count = 1  # 1st block is a divider, so we start our count from 1

        self._post(text=f"Updated on {timestamp}", kind="heading_2", index=count)

        for data in content.values():
            count += 1  # account for the divider in between

            # guaranteed that each data dict contains two keys "Date" and "Time"
            date, time = data.pop("Date"), data.pop("Time")
            data_timestamp = f"Timestamp: {date} {time}"

            # params must be present on the Notion page in data dict insertion order
            for param, value in data.items():
                count += 1
                self._post(text=f"{param}: {value}", kind="heading_1", index=count)

            count += 1
            self._post(text=data_timestamp, kind="paragraph", index=count)

        logger.debug(f"Posted data to Notion page with {timestamp = }.")

    def _post(self, text, kind, index):
        """internal method to post a no-frills simple block with the given text and kind (type) and block_id given by index"""
        # only works if Notion page structure remains unchanged
        block = {
            "type": kind,
            kind: {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "color": "default",
            },
        }
        block_id = self._page_data["results"][index]["id"]
        self._client.blocks.update(block_id=block_id, **block)
