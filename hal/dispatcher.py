""" This module contains helpers that dispatch data via Notion's api. """

from pathlib import Path

import notion_client as notion

from hal.logger import logger

# token.txt must be present at this path with two comma separated values: token, url
TOKENPATH = Path.cwd().parent / "token.txt"


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
        self._client.blocks.update(block_id=block_id, **block)
