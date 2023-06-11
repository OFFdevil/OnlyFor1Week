from geometry.equatorial import Equatorial

# спектральный класс звезды - по сути ее цвет. О -голубой, А - белый и тд
SPECTRAL_CLASSES = ('', 'O', 'B', 'A', 'F', 'G', 'K', 'M')
SPECTRAL_COLORS = (
    '00ff00', '9aafff', 'cad7ff', 'f8f7ff', 'fff4ea', 'fff2a1', 'ffc46f',
    'ff6060')  # для каждой буквы задаем соотв. цвет
SPECTRAL_MAP = {SPECTRAL_CLASSES[i]: SPECTRAL_COLORS[i] for i in range(0, len(SPECTRAL_CLASSES))}


# SPECTRAL_MAP - словарь с парами название-цвет

class Star:
    # звезда характеризуется позицией в екватор. системе, созвездием, магнитудой, цветом и названием
    def __init__(self, pos: Equatorial,
                 constellation, magnitude, spectral_class, name):
        self._position = pos
        self._constellation = constellation
        self._magnitude = magnitude
        self._spectral_class = spectral_class
        self._name = name
        if constellation is None or pos is None or magnitude is None or spectral_class is None or name is None:
            raise ValueError()
        self._hash = hash(pos)
        self._hpos = pos.to_horizontal_system(0, 0)

        @property
        def hpos(self):
            return self._hpos

    # геттеры
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
