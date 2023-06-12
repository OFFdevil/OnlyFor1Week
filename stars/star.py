from geometry.equatorial import Equatorial

"""Спектральный класс звезды - по сути ее цвет. О -голубой, А - белый и тд"""
"""SPECTRAL_MAP - словарь с парами символ- код цвета"""
SPECTRAL_MAP = {'': '00ff00', 'B': 'cad7ff',
                'O': '9aafff', 'K': 'ffc46f',
                'M': 'ff6060', 'F': 'fff4ea',
                'A': 'f8f7ff', 'G': 'fff2a1'}


class Star:
    # звезда характеризуется позицией в экватор. системе, созвездием, магнитудой, цветом и названием
    def __init__(self, pos: Equatorial, constellation, magnitude, spectral_class, name):
        self._position = pos
        self._constellation = constellation
        self._magnitude = magnitude
        self._spectral_class = spectral_class
        self._name = name
        if constellation is None or pos is None or magnitude is None or spectral_class is None or name is None:
            raise ValueError()
        self._hash = hash(pos)

    # геттеры
    @property
    def hpos(self):
        return self._hpos

    @property
    def position(self):
        return self._position

    @property
    def constellation(self):
        return self._constellation

    @property
    def name(self):
        return self._name

    @property
    def magnitude(self):
        return self._magnitude

    @property
    def spectral_class(self):
        return self._spectral_class

    def __str__(self):
        return "{{{}.{}: {}, {}}}".format(self.constellation, self.name, self.spectral_class, self.magnitude)

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return self.position == other.position and self.constellation == other.constellation
