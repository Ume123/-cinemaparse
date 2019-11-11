"""файл с классом CinemaParser"""

import time
import requests
from bs4 import BeautifulSoup

class CinemaParser:
    """ Класс нужен для оперирования с сайтом https://msk.subscity.ru/ """
    def __init__(self, name):
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
        """Функция ищет ссылку на фильм по его названию и выводит ближайщий"""
        if not self.content:
            self.extract_raw_content()
        for data in self.content.find_all('div', class_="movie-plate"):
            if data['attr-title'] == film_name:
                next_session_time = data['attr-next-screening']
                next_session_time_translation = time.ctime(int(i['attr-next-screening']))
                div_with_href = (i.find('div', class_='text-center movie-poster-mobile'))
                a_with_href = div_with_href.find('a')['href']
                link = self.url + a_with_href

        try:
            a = link
        except  UnboundLocalError:
            return (None, None)

        new_page = requests.get(link)
        page_film = BeautifulSoup(new_page.text, "html.parser")

        for first_table in page_film.find_all('tr', class_="row-entity"):
            table_with_time = first_table.find('td', class_='text-center cell-screenings')
            if table_with_time['attr-time'] == next_session_time:
                name_film = first_table.find('a', class_="underdashed").get_text()

        return name_film, next_session_time_translation

    def get_nearest_session(self):
#        if not self.content:
#            self.extract_raw_content()
        page=page.read(page.html)
        self.content = BeautifulSoup(page, "html.parser")
        dict_times={}
        dict_movie_plates={}
        movie_plates=self.content.find_all('div', class_="movie-plate")
        print(movie_plates[0]['attr-next-screening'])
        for i in range(len(movie_plates)):
            dict_times.update({int(movie_plates[i]['attr-next-screening']):i})
            dict_movie_plates.update({movie_plates[i]:i})
       # print(dict_movie_plates)

#CINEMAPARSER = CinemaParser('Москва')
#print(CINEMAPARSER.get_films_list())
#print(CINEMAPARSER.get_nearest_session()