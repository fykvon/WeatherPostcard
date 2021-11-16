# -*- coding: utf-8 -*-


import datetime

import cv2

from models import DatabaseUpdater as db
from parsing_engine import WeatherParsing
from postcard_maker import ImageMaker


class WeatherPostcardMaker:
    """
    Does the parsing for period and creates the postcard from DataBase

    """
    def __init__(self):
        self.select_date = datetime.datetime.today().strftime('20%y-%m-%d')
        self.list_with_steps = ['Спарсить информацию в базу данных', 'Распечатать открытку',
                                'Вывести результат на консоль', 'Закончить']
        self.day_info_list = []

    def parsing_weather(self) -> list:
        """
        This method requests dates from the user

        :return: list of dictionaries
        """
        while True:
            try:
                user_input_from = input('Введите начальную дату парсинга в формате ГГГГ-ММ-ДД: ')
                user_input_to = input('Введите конечную дату парсинга в формате ГГГГ-ММ-ДД: ')
                parsing_weather = WeatherParsing(user_input_from=user_input_from, user_input_to=user_input_to)
                parsing_weather_date = parsing_weather.main()
                return parsing_weather_date
            except:
                print('Неверный ввод даты. Введите ГГГГ-ММ-ДД!')

    def database_update(self, parsing_weather_date):
        """
        Create and update DataBase

        :param parsing_weather_date: list this weather info
        """
        try:
            albums_in_db = db.insert_many(parsing_weather_date).execute()
        except:
            for days in parsing_weather_date:
                day = days.get('Date')
                min_temp = days.get('Min_temp')
                max_temp = days.get('Max_temp')
                day_details = days.get('Day_details')

                albums_in_db = (
                    db.insert(Date=day, Min_temp=min_temp, Max_temp=max_temp, Day_details=day_details).on_conflict(
                        conflict_target=[db.Date],
                        update={db.Day_details: day_details}).execute())
        return albums_in_db

    def create_image(self, weather_info: list):
        """
        This method should get a list with weather information and create an image

        :param weather_info: list this weather info
        :return: None
        """
        image_maker = ImageMaker(weather_data=weather_info)
        image_maker.main()

    def select_day_for_postcard(self) -> list:
        """
        This method implements logic for selecting information from the database and returning a list
        with weather information for the selected period

        """
        self.day_info_list = []
        not_in_db_day = []
        days_in_db = []
        while True:
            user_input_from = input('Введите начальную дату печати: ')
            user_input_to = input('Введите конечную дату печати: ')
            user_input_from = datetime.date.fromisoformat(user_input_from)
            user_input_to = datetime.date.fromisoformat(user_input_to)
            delta = user_input_to - user_input_from
            int_delta = int(delta.days) + 1
            n = 0
            for days in range(int_delta):
                select_day = user_input_from + datetime.timedelta(days=n)
                select_day = select_day.isoformat()
                n += 1
                for day in db.select():
                    if select_day in day.Date:
                        days_in_db.append(day.Day_details)
                        self.day_info_list.append([day.Day_details, day.Min_temp, day.Max_temp, select_day])
                not_in_db_day.append(select_day)
            for info in self.day_info_list:
                not_in_db_day.remove(info[3])
            for day in not_in_db_day:
                print('Даты ', day, 'нет в базе данных')
            return self.day_info_list

    def print_steps(self):
        """
        Simple print in cicle

        """
        print('Выберите действие')
        for i, step in enumerate(self.list_with_steps):
            i += 1
            print(i, step)
        user_input = int(input())
        return user_input

    def main(self):
        """
        Main function

        """
        while True:
            step = self.print_steps()
            if step == 1:
                parsing_for_database = self.parsing_weather()
                self.database_update(parsing_for_database)
            elif step == 2:
                try:
                    date_for_postcard = self.select_day_for_postcard()
                    for iday in date_for_postcard:
                        self.create_image(weather_info=iday)
                    cv2.destroyAllWindows()
                except:
                    print('Такой даты нет в БД. Сначала заполните БД')
            elif step == 3:
                try:
                    select_date = self.select_day_for_postcard()
                    for iday in select_date:
                        print(f'******************\nDay details: {iday[0]}\nMinimum temperature: {iday[1]}\n'
                              f'Maximum temperature: {iday[2]}\nDate: {iday[3]}\n*********************')
                except:
                    print('Такой даты нет в БД. Сначала заполните БД')
            elif step == 4:
                return False


if __name__ == '__main__':
    parsing_weather = WeatherPostcardMaker()
    parsing_weather.main()
