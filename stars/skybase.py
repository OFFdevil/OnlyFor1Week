import datetime

from geometry.avector import Equatorial
from stars.star import Star


class SkyBase:
    def __init__(self, stars):  # инициализация
        self._stars = stars
        self._constellations = {star.constellation: [] for star in stars}  # созвездия - это массив звезд
        for star in stars:
            self._constellations[star.constellation].append(star)

    @property
    def constellations(self):  # геттер.
        return self._constellations.keys()  # функция keys по сути возвращает ключи словаря

    def get_stars(self, constellations):
        stars = []
        for constellation in constellations:
            if not constellation in self._constellations:
                continue
            for star in self._constellations[constellation]:
                stars.append(star)
            return stars
