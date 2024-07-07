import requests
import pandas as pd

from . import Parser


class MPGU(Parser):
    def __init__(self, vuz_name: str):
        super().__init__(vuz_name)

        # Здесь указываются запросы, с помощью которых можно получать таблицы.
        # Чтобы их получить, откройте меню разработчика в браузере, в нём панель "Сети",
        # перезагрузите страницу и найдите запрос, ответ на который - таблица с данными.
        self.urls = [
            (
                'Институт детства. Факультет начального образования',
                'https://epk24.mpgu.su/ajax/interactive_detail',
                {
                    'report_option': '00f56aba-2e61-11ef-9781-00155d017103',
                    'scenario': '337e6e8a-da16-11ee-977b-00155d102600',
                    'scenarioN': 'Бакалавриат/специалитет/базовое высшее образование Головной вуз 2024',
                    'level_education': '9ea44618-fbf6-11ee-977e-00155d102600',
                    'form_education': '62575a1f-da07-11ee-977b-00155d102600',
                    'basis_admission': '62575a1a-da07-11ee-977b-00155d102600|false',
                    'faculty': 'd835f80a-dcfe-11ed-94d7-00155d833208',
                    'direction': 'bea18d72-a3cb-11ee-94f9-00155d833208',
                    'profile': '1ab894a6-b936-11ee-94f9-00155d833208',
                    'actions': 'list_applicants'
                }
            ),
            (
                'Институт социально-гуманитарного образования',
                'https://epk24.mpgu.su/ajax/interactive_detail',
                {
                    'report_option': '00f56aba-2e61-11ef-9781-00155d017103',
                    'scenario': '337e6e8a-da16-11ee-977b-00155d102600',
                    'scenarioN': 'Бакалавриат/специалитет/базовое высшее образование Головной вуз 2024',
                    'level_education': '9ea44618-fbf6-11ee-977e-00155d102600',
                    'form_education': '62575a1f-da07-11ee-977b-00155d102600',
                    'basis_admission': '62575a1a-da07-11ee-977b-00155d102600|false',
                    'faculty': 'e70d4005-b75d-11ed-94d3-00155d833208',
                    'direction': 'bea18d72-a3cb-11ee-94f9-00155d833208',
                    'profile': 'f4d4b6cb-b92f-11ee-94f9-00155d833208',
                    'actions': 'list_applicants'
                }
            )
        ]

    # Делает запрос и получает записи таблицы в формате json
    def __get_program_json(self, url: str, params: dict) -> dict:
        # Выполнение запроса
        response = requests.get(url, params=params)

        # Проверка статуса ответа и вывод данных
        if response.status_code == 200:
            # Если ответ в формате JSON
            try:
                data = response.json()
                return data
            except ValueError:
                # Если ответ не в формате JSON, выводим как текст
                return f"Error: Ответ сервера не имеет json формат"
        else:
            return f"Error: {response.status_code}"

    # Преобразует json в формат pandas DataFrame
    def __get_program_df(self, program_name: str, json_table: dict) -> pd.DataFrame:
        to_df = {
            'snils': [],
            'score': [],
            'original': [],
            self.vuz_name: [],
            'program_name': [],
            'priority': []
        }

        for person in json_table['data']['list_applicants']:
            to_df['snils'].append(person['УникальныйКод'])
            to_df['score'].append(person['СуммаБаллов'])
            to_df['original'].append(self.vuz_name if person['Оригинал'] == 'Да' else '')
            to_df['priority'].append(person['Приоритет'])
            to_df[self.vuz_name].append(1)
            to_df['program_name'].append(program_name)

        return pd.DataFrame(to_df)

    # Собирает данные с таблиц разных напралений в один pandas DataFrame
    def get_table(self):
        dfs = []

        for program_name, url, params in self.urls:
            dfs.append(self.__get_program_df(program_name, self.__get_program_json(url, params)))

        return pd.concat(dfs, ignore_index=True)
