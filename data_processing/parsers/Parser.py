class Parser:
    def __init__(self, vuz_name: str):
        self.vuz_name = vuz_name

    def get_table(self):
        raise NotImplementedError('You must implement the GetTable method!')
