import math
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPen


def sign(n):  # знак числа n
    return -1 if n < 0 else (0 if n == 0 else 1)


class RenderSettings:
    def __init__(self):
        self.fisheye = True  # для обзора - чтобы было искажение рыбьего глаза
        # задаем цвета
        self._earth_color = QColor(0, 100, 100)
        self._star_color = QColor(255, 255, 255)
        self._sky_color = QColor(0, 0, 0)
        self._up_color = QColor(255, 0, 255)
        self._down_color = QColor(0, 255, 255)
        # создает кисть для окрашивания области, которая соответствует объекту
        # кортеж является набором инструментов, которые используем для отрисовки объектов
        self._earth_drawer = (QBrush(self._earth_color), QPen(self._earth_color))
        self._star_drawer = (QBrush(self._star_color), QPen(self._star_color))
        self._sky_drawer = (QBrush(self._sky_color), QPen(self._sky_color))
        self._up_drawer = (QBrush(self._up_color), QPen(self._up_color))
        self._down_drawer = (QBrush(self._down_color), QPen(self._down_color))

    def get_drawer(self, color_name: str):  # шаблон для создания имен соответствующих
        # атрибутов
        fullname = "_" + color_name + "_drawer"
        return self.__getattribute__(fullname)

    def apply_color(self, name: str, painter: QPainter):  # шаблон для применения какого-то
        # цвета
        b, p = self.get_drawer(name)
        painter.setBrush(b)
        painter.setPen(p)


class ControllableRenderSettings:  # класс, который сохраняет настройки
    # которые связаны с отображением изображения
    def __init__(self):
        self.fps = 30
        self.speed = 1
        self.zoom = 1

    @property
    def speed_rank(self):  # ранг для скорости текущего объекта
        # в зависимости от ее значения.
        if self.speed == 0:
            return 0
        return (math.log10(abs(self.speed)) + 1) * sign(self.speed)

    @speed_rank.setter
    def speed_rank(self, value):
        # автоматически вычисляет и изменяет
        # значение атрибута speed в соответствии с заданным значением.
        if value > 10:
            raise ValueError()
        self.speed = 10 ** (abs(value) - 1) * sign(value)
        # новое значение атрибута speed
        # в зависимости от значения атрибута speed_rank.
