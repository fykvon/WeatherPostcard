from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup as bs
import requests


class WeatherParsing:
    """
    Parsing weather info from www.darksky.net

    """

    def __init__(self, user_input_from, user_input_to):
        self.user_input_from = user_input_from
        self.user_input_to = user_input_to
        self.user_date = []
        self.dates = []
        self.weather_data = []
        self.date = str

    def date_for_parsing(self) -> list:
        user_input_from = date.fromisoformat(self.user_input_from)
        user_input_to = date.fromisoformat(self.user_input_to)
        delta = user_input_to - user_input_from
        int_delta = int(delta.days)
        self.dates.append(str(user_input_from))
        n = 0
        for days in range(int_delta):
            n += 1
            day_by_day = user_input_from + timedelta(days=n)
            self.dates.append(date.isoformat(day_by_day))
        return self.dates

    def get_html(self, date: str):
        r = requests.get(f'https://darksky.net/details/55.6787,37.2585/{date}/us12/en')
        return r

    def weather_parsing(self, r):
        soup = bs(r.text, 'html.parser')
        find_max_temp = soup.find('span', class_='lowTemp swap').find('span', class_='temp').text
        len_find_max_temp = len(find_max_temp)
        find_max_temp = find_max_temp[0:len_find_max_temp - 1]
        find_min_temp = soup.find('span', class_='highTemp swip').find('span', class_='temp').text
        len_find_min_temp = len(find_min_temp)
        find_min_temp = find_min_temp[0:len_find_min_temp - 1]
        find_daydetails = soup.find('div', class_="dayDetails center").find('p').text.replace(u'\xa0', ' ')
        if find_daydetails == None:
            raise Exception('find_daydetails is None')
        json = {
            'Date': self.date,
            'Min_temp': find_min_temp,
            'Max_temp': find_max_temp,
            'Day_details': find_daydetails
        }

        self.weather_data.append(json)

    def main(self):
        self.date_for_parsing()
        for date in self.dates:
            r = self.get_html(date)
            self.date = date
            self.weather_parsing(r)
        return self.weather_data
