import datetime

from geometry.avector import Equatorial
from stars.star import Star


class SkyBase:  # класс-база данных со всеми звездами
    def __init__(self, stars):  # атрибуты классы - звезды и созвездия
        self._stars = stars
        self._constellations = {star.constellation: [] for star in stars}  # созвездие - это массив звезд
        for star in stars:
            self._constellations[star.constellation].append(star)

    @property
    def constellations(self):  # геттер.
        return self._constellations.keys()  # функция keys по сути возвращает ключи словаря(то есть названия созвездий)

    def get_stars(self, avaible_constellations: set):  # передаем set из созвездий
        stars = []
        for constellation in avaible_constellations:
            if not constellation in self._constellations:
                continue
            for star in self._constellations[constellation]:  # и из всех выбираем только те
                stars.append(star)
            return stars
