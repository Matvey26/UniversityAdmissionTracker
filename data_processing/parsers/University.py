import pandas as pd

from typing import Dict


class University:
    def __init__(self, vuz_name: str, short_vuz_name: str):
        self.vuz_name = vuz_name
        self.short_name = short_vuz_name

    def get_table(self) -> Dict[str, pd.DataFrame]:
        raise NotImplementedError('You must implement the GetTable method!')

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.vuz_name == other or self.short_name == other
        elif isinstance(other, University):
            return self.vuz_name == other.vuz_name
        return False
