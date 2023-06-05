from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPen


class RenderSettings:
    def __init__(self):
        # задаем цвета
        self._earth_color = QColor(0, 100, 100)
        self._star_color = QColor(255, 255, 255)
        self._sky_color = QColor(0, 0, 0)
        self._point_color = QColor(255, 0, 255)
        # создает кисть для окрашивания области, которая соответствует объекту
        # кортеж является набором инструментов, которые используем для отрисовки объектов
        self._earth_drawer = (QBrush(self._earth_color), QPen(self._earth_color))
        self._star_drawer = (QBrush(self._star_color), QPen(self._star_color))
        self._sky_drawer = (QBrush(self._sky_color), QPen(self._sky_color))
        self._point_drawer = (QBrush(self._point_color), QPen(self._point_color))

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
