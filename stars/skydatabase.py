import datetime

from geometry.equatorial import Equatorial
from stars.filter import Filter
from stars.star import Star


class SkyDataBase:  # класс-база данных со всеми звездами
    def __init__(self, stars):  # атрибуты классы - звезды и созвездия
        consts = {star.constellation: [] for star in stars}  # созвездия - это массивы звезд
        for star in stars:
            consts[star.constellation].append(star)
        self._constellations = {}
        self._names = set()
        for cn in consts.keys():
            self._constellations[cn] = tuple(consts[cn])
            for s in self._constellations[cn]:
                self._names.add(s.name)

    @property
    def constellations(self):  # геттер.
        return self._constellations.keys()  # функция keys по сути возвращает ключи словаря(то есть названия созвездий)

    def get_stars(self, selection: Filter):  # возвращает звезды данных созвездий(передаем Filter)
        stars = []
        for constellation in selection.constellations:  # получаем звезды из выбранных созвездий
            if constellation not in self._constellations:  # если переданного созвездия не существует
                continue
            for star in self._constellations[constellation]:  # добавляем все звезды всех выбранных созвездий
                stars.append(star)
            return stars
