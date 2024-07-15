import pandas as pd
import time

from .parsers import MPGU, MSLU, University
from matplotlib import pyplot as plt
from typing import List


class TableInterface:
    def __init__(self):
        self.unis = [
            MPGU('Московский педагогический государственный университет', 'mpgu'),
            MSLU('Московский государственный лингвистический университет', 'mslu')
        ]

    def get_vuz_list(self) -> List[University]:
        return self.unis

    def get_vuz_by_name(self, name: str) -> University:
        for vuz in self.unis:
            if vuz == name:
                return vuz
        return None

    def save_score_histogram_picture(self, vuz: University):
        data = vuz.get_table()
        paths = []
        for program_name, df in data.items():
            scores = [int(i) for i in df['score'].tolist() if int(i) > 50]
            plt.hist(scores, bins=50)
            plt.title(program_name)
            plt.xlabel('Сумма балов ЕГЭ')
            plt.ylabel('Количество людей')
            path = f'data_processing/temp/{program_name}{int(time.time())}.png'
            paths.append(path)
            plt.savefig(path)
            plt.close()

        return paths

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError('Тип ключа должен быть целым числом!')

        if key < 0 or key >= len(self.unis):
            raise LookupError('Выход за пределы списка!')

        return self.unis[key]
