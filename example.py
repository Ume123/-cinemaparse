""" Пример использования класса CinemaParser"""
from cinemaparser import CinemaParser
CINEMAPARSER = CinemaParser('Москва')
print(CINEMAPARSER.get_films_list())
print(CINEMAPARSER.get_first_session('Джокер'))
