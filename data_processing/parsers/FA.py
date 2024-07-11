import requests

from . import Parser


class FA(Parser):
    def __init__(self, vuz_name: str):
        super().__init__(vuz_name)

    def parse(self, url: str, params: dict):
        page = requests.post(url, params)
        if page.status_code != 200:
            return f"Error: {page.status_code}"
        
        try:
            return page.json()
        except ValueError:
            return page.text