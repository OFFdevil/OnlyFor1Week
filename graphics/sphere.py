from PyQt5.QtGui import QColor

from vectors.vector import Vector


class Sphere:  # класс сфера - 3д сферический объект
    def __init__(self, radius: int):  # создали сферу с данными параметрами
        self.radius = radius  # радиус сферы
        self.centre = Vector(0, 0, 0)  # вектор, указывающий на центр сферы
        self.color = (128, 0, 0)  # задали цвет сферы
# код определяет минимальное количество атрибутов, которые нужна, чтобы задать сферу
