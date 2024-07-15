import requests
import pandas as pd

from bs4 import BeautifulSoup
from . import University


class MSLU(University):
    def __init__(self, vuz_name: str, short_vuz_name: str):
        super().__init__(vuz_name, short_vuz_name)
        self.urls = [
            (
                '39.03.01 Социология',
                'https://linguanet.ru/docs/1796356130249721111.html'
            ),
            (
                '40.03.01 Юриспруденция',
                'https://linguanet.ru/docs/1796356328385496343.html'
            )
        ]

    def __get_program_df(self, url: str):
        page = requests.get(url)
        if page.status_code != 200:
            return f"Error: {page.status_code}"

        soup = BeautifulSoup(page.content.decode('utf-8'), 'lxml')
        try:
            table = soup.find_all('table')[1]
        except Exception as e:
            return f"Error: На странице не найдена нужная таблица\n{e}"

        to_df = {
            'snils': [],
            'score': [],
            'original': [],
            'priority': []
        }

        for i in table.find_all('tr'):
            elements = [j.text for j in i.find_all('td')]
            if len(elements) != 13:
                continue
            to_df['snils'].append(elements[1])
            score = elements[2]
            try:
                score = int(score)
            except ValueError:
                score = 0
            to_df['score'].append(score)
            to_df['original'].append(int(elements[10] != 'Нет'))
            to_df['priority'].append(elements[11])

        return pd.DataFrame(to_df)

    def get_table(self):
        dfs = {}

        for prog_name, url in self.urls:
            dfs[prog_name] = self.__get_program_df(url)

        return dfs
