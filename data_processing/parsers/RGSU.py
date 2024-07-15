import requests
import pandas as pd

from bs4 import BeautifulSoup
from typing import Dict
from . import University


class RGSU(University):
    def __init__(self, vuz_name: str, short_vuz_name: str):
        super().__init__(vuz_name, short_vuz_name)
        self.urls = (
            (
                'Государственное и муниципальное управление',
                'https://rgsu.net/abitur/bachelor/spiski-lits-podavshih-dokumenty/',
                {
                    'level': '2',
                    'city': 'Анапа',
                    'receipt': 'На общих основаниях',
                    'direction': 'Государственное и муниципальное управление (бакалавриат)',
                    'directionsasp': 'Управление государственными и муниципальными услугами и заказами',
                    'eform': 'Очно-заочная',
                    'foundation': 'Полное возмещение затрат'
                }
            ),
        )
    
    def __get_program_df(self, url: str, params: dict) -> pd.DataFrame:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return f"Error: {response.status_code}"
        
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find('table')

        to_df = {
            'snils': [],
            'score': [],
            'original': [],
            'priority': []
        }

        kek = []
        for i in table.find_all('tr'):
            elements = [j.text for j in i.find_all('td')]
            if len(elements) < 11:
                continue
            to_df['snils'].append(elements[1])
            to_df['score'].append(elements[6])
            to_df['original'].append(int(elements[9] != 'Нет'))
            to_df['priority'].append(int(elements[10]))
        
        return pd.DataFrame(to_df)
        

    def get_table(self) -> Dict[str, pd.DataFrame]:
        dfs = {}
        for program_name, url, params in self.urls:
            dfs[program_name] = self.__get_program_df(url, params)
        
        return dfs