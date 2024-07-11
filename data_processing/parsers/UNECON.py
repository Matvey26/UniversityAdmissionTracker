import requests

from . import Parser


class UNECON(Parser):
    def get_html_page(self):
        params = {
			"filial_kod": "1",
			"zayav_type_kod": "1",
			"obr_konkurs_kod": "0",
			"recomend_type": "null",
			"rec_status_kod": "all",
			"ob_forma_kod": "1",
			"ob_osnova_kod": "1",
			"konkurs_grp_kod": "4647",
			"prior": "all",
			"status_kod": "all",
			"is_orig_doc": "all",
			"dogovor": "all",
			"show": "Показать"
		}
        response = requests.get('https://priem.unecon.ru/stat/stat_konkurs.php', params)

        if response.status_code == 200:
            return response.text
        return f"Error: {response.status_code}, {response.content.decode('utf-8')}"