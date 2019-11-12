"""файл с классом CinemaParser"""

import time
import requests
from bs4 import BeautifulSoup

class CinemaParser:
    """ Класс нужен для оперирования с сайтом https://msk.subscity.ru/ """
    def __init__(self, name=" "):
        """Функция используется для получения html страницы сайта"""
        self.city = name
        if self.city == "Москва":
            self.url = 'https://msk.subscity.ru/'
        else:
            self.url = 'https://spb.subscity.ru/'

        self.content = None

    def extract_raw_content(self):
        """Функуия Скачивает главную страницу"""
        page = requests.get(self.url)
        self.content = BeautifulSoup(page.text, "html.parser")

    def print_raw_content(self):
        """Функция выводит html на экран"""
        if not self.content:
            self.extract_raw_content()
        return self.content.prettify()

    def get_films_list(self):
        """Функция используется для поиска фильмов"""
        if not self.content:
            self.extract_raw_content()
        list_films = []
        for i in self.content.find_all('div', class_="movie-title-original"):
            list_films.append(i.text)
        return list_films

    def dssddssd(self, film_name):
        """Функция ищет ссылку на фильм по его названию и выводит ближайщий"""
        link = ''
        if not self.content:
            self.extract_raw_content()
        for i in self.content.find_all('a', class_="underdashed"):
            if i.text.replace('­', '') == film_name:
                print(1)
                link = i['href']
        link = 'https://msk.subscity.ru' + link
        return link

    def get_first_session(self, film_name):
        """Функция ищет ссылку на фильм по его названию и выводит ближайщий сеанс и кинотеатр"""
        if not self.content:
            self.extract_raw_content()
        for data in self.content.find_all('div', class_="movie-plate"):
            if data['attr-title'] == film_name:
                next_session_time = data['attr-next-screening']
                next_session_time_translation = time.ctime(int(data['attr-next-screening']))
                div_with_href = (data.find('div', class_='text-center movie-poster-mobile'))
                a_with_href = div_with_href.find('a')['href']
                link = self.url + a_with_href

        try:
            per = link
        except  UnboundLocalError:
            return (None, None)

        new_page = requests.get(link)
        page_film = BeautifulSoup(new_page.text, "html.parser")
        for first_table in page_film.find_all('tr', class_="row-entity"):
            table_with_time = first_table.find('td', class_='text-center cell-screenings')
            if int(table_with_time['attr-time']) == int(next_session_time):
                name_cinema = first_table.find('a', class_="underdashed").get_text()

        return name_cinema, next_session_time_translation

    def get_soonest_session(self):
        """Функция используется для поиска ближайшего сеанса и кинотеатра"""
        if not self.content:
            self.extract_raw_content()
        dict_movie_plates = {}
        times = []
        movie_plates = self.content.find_all('div', class_="movie-plate")
        for movie_plate in movie_plates:
            dict_movie_plates.update({int(movie_plate['attr-next-screening']):movie_plate})

        storted_times = sorted(dict_movie_plates.keys())
        soonest_plate = dict_movie_plates.get(storted_times[0])

        div_with_href = (soonest_plate.find('div', class_='text-center movie-poster-mobile'))
        a_with_href = div_with_href.find('a')['href']
        link = self.url + a_with_href

        new_page = requests.get(link)
        page_film = BeautifulSoup(new_page.text, "html.parser")
        for first_table in page_film.find_all('tr', class_="row-entity"):
            table_with_time = first_table.find('td', class_='text-center cell-screenings')
            times.append(table_with_time['attr-time'])
            if int(table_with_time['attr-time']) == storted_times[0]:
                name_cinema = first_table.find('a', class_="underdashed").get_text()
        try:
            per = name_cinema
        except  UnboundLocalError:
            return (None, None, None)

        return (name_cinema, soonest_plate['attr-title'], time.ctime(int(storted_times[0])))

