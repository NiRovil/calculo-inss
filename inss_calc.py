from datetime import datetime

import pandas as pd
import requests

_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.188/dados?formato=json"

class Inpc():

    def __init__(self, inicial_date: str, final_date: str) -> None:
        self._url = _url
        self._inicial = inicial_date
        self._final = final_date
        self._json = self.call(_url)
        self._dates = self.find_date()
        self._result = self.calc()

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

        date_format = '%d/%m/%Y'

        inicial_date = datetime.strptime(self._dates['inicial_date'], date_format)
        final_date = datetime.strptime(self._dates['final_date'], date_format)

        months_to_calc = (final_date.year - inicial_date.year) * 12 + (final_date.month - inicial_date.month)

        print(f'For this operation you need to provide {months_to_calc} values, who match the exact amout of months corresponding.')
        print('If you want, you can upload a CSV file with all months and its respective values.')

        df = pd.read_excel('values.xls')
        value_list = []

        for index, row in df.iterrows():
            month = row['Month']
            for col in df.columns[1:]:
                year = int(col)
                value = row[col]
                value_list.append({'year': year, 'month': month,'value': value})
        
        #for i in value_list:
            #print(i)

        return 'Nothing'