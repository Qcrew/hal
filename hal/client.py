""" Implements subset of Notion API specific to HAL'S functioning """

import time

import requests

from hal.config import DELAY, FRIDGE_NAME, NOTION_TOKENPATH, PARAMS
from hal.logger import logger
from hal.param import Param


class Client:
    """ """

    BASE_URL: str = "https://api.notion.com/v1"

    def __init__(
        self,
    ) -> None:
        """ """
        with NOTION_TOKENPATH.open() as tokenfile:
            self._token: str = tokenfile.read()

        self._headers: dict[str, str] = {
            "Authorization": "Bearer " + self._token,
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

        self._database_id: str = self._get_database_id()
        logger.info(f"Notion client connected to database with id: {self._database_id}")
        self._page_map: dict[Param, str] = self._get_page_map()
        self._update_page()  # update page name and category

    def _get_database_id(self) -> str:
        """get database id based on fridge_name"""
        url = Client.BASE_URL + "/search"
        payload = {"query": FRIDGE_NAME}
        response = requests.post(url, json=payload, headers=self._headers)
        return response.json()["results"][0]["id"]

    def _get_page_map(self) -> dict[str, str]:
        """return dict with key = param name and value = page id"""
        url = Client.BASE_URL + f"/databases/{self._database_id}/query"
        pages = requests.post(url, headers=self._headers).json()["results"]
        return dict(zip(PARAMS, [p["id"] for p in pages]))

    def _update_page(self):
        """ """
        payload = {
            "properties": {
                "Parameter": {"title": [{"text": {}}]},
                "Category": {"multi_select": [{}]},
            }
        }
        for param, page_id in self._page_map.items():
            name, category = param.name, param.category
            url = Client.BASE_URL + f"/pages/{page_id}"
            payload["properties"]["Parameter"]["title"][0]["text"]["content"] = name
            payload["properties"]["Category"]["multi_select"][0]["name"] = category
            requests.patch(url, json=payload, headers=self._headers)
            logger.info(f"Updated {name = } and {category = } at {page_id = }")
            time.sleep(DELAY)

    def _errorcheck(self, response: requests.Response) -> bool:
        """ """  # TODO complete it
        if response.status_code == 200:
            return True
        else:
            logger.error(f"{response}: {response.text}")
            return False

    def post(self, param: Param, value: str) -> bool:
        """ """
        page_id = self._page_map[param]
        url = Client.BASE_URL + f"/pages/{page_id}"
        data = {"properties": {"Value": {"rich_text": [{"text": {"content": value}}]}}}
        response = requests.patch(url, json=data, headers=self._headers)
        return self._errorcheck(response)
