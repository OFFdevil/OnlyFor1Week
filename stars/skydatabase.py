import datetime

from geometry.avector import Equatorial
from stars.star import Star


class SkyDataBase:  # класс-база данных со всеми звездами
    def __init__(self, stars):  # атрибуты классы - звезды и созвездия
        self._stars = stars
        self._constellations = {star.constellation: [] for star in stars}  # созвездие - это массив звезд
        for star in stars:
            self._constellations[star.constellation].append(star)

    @property
    def constellations(self):  # геттер.
        return self._constellations.keys()  # функция keys по сути возвращает ключи словаря(то есть названия созвездий)

    def get_stars(self,
                  available_constellations: set):  # возвращает звезды данных созвездий(передаем set из созвездий)
        stars = []
        for constellation in available_constellations:
            if not constellation in self._constellations:  # если переданного созвездия не существует
                continue
            for star in self._constellations[constellation]:  # добавляем все звезды всех созвездий
                stars.append(star)
            return stars
