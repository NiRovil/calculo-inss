import requests

_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.188/dados?formato=json"

class Inpc():

    def __init__(self, inicial_date: str, final_date: str, values: list) -> None:
        self._url = _url
        self._inicial = inicial_date
        self._values = values
        self._final = final_date
        self._json = self.call(_url)
        self._dates = self.find_date()

    @staticmethod
    def call(url: str) -> str:
        req = requests.get(url)
        return req.json()

    def find_date(self) -> dict:

        dates = {'inicial_date': None, 'final_date': None}

        inicial = '01/' + self._inicial
        for date in self._json:
            if date['data'] == inicial:
                dates['inicial_date'] = date['data']
                break

        final = '01/' + self._final
        for date in self._json:
            if date['data'] == final:
                dates['final_date'] = date['data']
                break

        if dates['inicial_date'] is None or dates['final_date'] is None:
            return print(f'The inicial and the final date must be between: {self._json[0]["data"]} and {self._json[-1]["data"]}')

        return dates

    def calc(self):

        pass