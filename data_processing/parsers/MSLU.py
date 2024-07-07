import requests
import pandas as pd

from bs4 import BeautifulSoup
from . import Parser

class MSLU(Parser):
    def __init__(self, vuz_name: str):
        super().__init__(vuz_name)
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
    
    def __get_program_df(self, program_name: str, url: str):
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
            'vuz_name': [],
            'priority': [],
            'program_name': []
        }

        for i in table.find_all('tr'):
            elements = [j.text for j in i.find_all('td')]
            if len(elements) != 13:
                continue
            to_df['snils'].append(elements[1])
            to_df['score'].append(elements[2])
            to_df['original'].append(elements[10])
            to_df['priority'].append(elements[11])
            to_df['vuz_name'].append(self.vuz_name)
            to_df['program_name'].append(program_name)
            
        return pd.DataFrame(to_df)
    
    def get_table(self):
        dfs = []
        for prog_name, url in self.urls:
            dfs.append(self.__get_program_df(prog_name, url))
        
        return pd.concat(dfs, ignore_index=True)