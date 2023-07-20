from datetime import datetime

import PySimpleGUI as sg
import pandas as pd
import requests

from suport_dates import *

_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.188/dados?formato=json"

class Inpc():

    def __init__(self, inicial_date: str, final_date: str) -> None:
        self.menu()
        self._url = _url
        self._inicial = inicial_date
        self._final = final_date
        #self._json = self.call(_url)
        #self._dates = self.find_date()
        #self._result = self.calc()

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
    
    def menu(self):

        sg.theme('dark grey 9')

        layout = [
            [sg.Text('Welcome to the calculator!')],
            [sg.Text('Which period do you need to calculate?')],
            [sg.Text('From'), sg.Combo(MONTHS), sg.Combo(YEARS)],
            [sg.Text('To'), sg.Combo(MONTHS), sg.Combo(YEARS)],
            [sg.Text(size=(40,1), key='-OUTPUT-', text_color='red')],
            [sg.Button('Calculate'), sg.Button('Quit')]
        ]

        window = sg.Window('Menu', layout)

        while True:

            event, values = window.read()

            print(values)
            if event == sg.WIN_CLOSED or event == 'Quit':
                break
            
            first_month = get_month(values[0])
            second_month = get_month(values[2])

            print(first_month, second_month)
            print(values[1], values[3])
            
            if (values[0] == values [2]) and (values[1] == values[3]):
                window['-OUTPUT-'].update("The date couldn't be the same!")

            if (first_month >= second_month) and (values[1] >= values[3]):
                window['-OUTPUT-'].update("The inicial date couldn't be lower or equal to the final date!")

            else:
                confirmation_layout = [
                    [sg.Text('You confirm the information?')],
                    [sg.Text(f'From {values[0]}/{values[1]} to {values[2]}/{values[3]}')],
                    [sg.Button('Confirm'), sg.Button('Back')]
                ] 
                confirmation_window = sg.Window('Menu', confirmation_layout)

                confirmation_event, confirmation_values = confirmation_window.read()
                
                if confirmation_event == 'Confirm':
                    confirmation_window.close()
                    window.close()
                    self.submenu()
                
                if confirmation_event == sg.WIN_CLOSED or confirmation_event == 'Back':
                    confirmation_window.close()
                    window['-OUTPUT-'].update('')

        window.close()

    def submenu(self):
        layout = [
            [sg.Text('Text')]
        ]

        window = sg.Window('SubMenu', layout)

        window.read()

    def calc(self):

        date_format = '%d/%m/%Y'

        inicial_date = datetime.strptime(self._dates['inicial_date'], date_format)
        final_date = datetime.strptime(self._dates['final_date'], date_format)

        months_to_calc = (final_date.year - inicial_date.year) * 12 + (final_date.month - inicial_date.month)

        print(f'For this operation you need to provide {months_to_calc} values, who match the exact amout of months corresponding.')
        print('If you want, you can upload a CSV file with all months and its respective values.')

        df = pd.read_excel('values.xls')
        df = df.fillna(0)
        value_list = []

        for index, row in df.iterrows():
            month = int(row['Month'])
            for col in df.columns[1:]:
                year = int(col)
                value = row[col]
                value_list.append({'year': year, 'month': month, 'value': value})
            
        
        
        print(value_list[23])
        return 'Nothing'