import math

from geometry.angle_helpers import to_0_360, to_cos_period_cutted
from geometry.nvector import NVector
from geometry.vector import Vector


class Horizontal(NVector):

    def __init__(self, a, h):  # TODO: все брать по модулю 360 и в -90 до 90 по умолчанию!!!!
        # инициализация координат точки в горизонтальной системе
        super().__init__((to_0_360(a), to_cos_period_cutted(h)))

    def to_point(self, radius=1) -> Vector:  # преобразует координаты точки из горизонтальной
        # системы (центр в точке, где стоит наблюдатель) в декартову систему (две перп оси)
        a = math.radians(-self.a)
        h = math.radians(self.h)
        z = radius * math.sin(h)
        r = math.sqrt(radius ** 2 - z ** 2)
        x = r * math.cos(a)
        y = r * math.sin(a)
        return Vector(x, y, z)

    def angle_to(self, other_point):  # определение угла между данным объектом horizontal и другой точкой
        return math.degrees(self.to_point().angle_to(other_point.to_point()))

    @property
    def a(self):  # получаем значение азимута
        return self[0]

    @property
    def h(self):  # получаем значение высоты
        return self[1]

    def __add__(self, other):  # складываем две координаты в горизонтальной системе
        return Horizontal(*self._add_(other))

    def __sub__(self, other):  # вычитаем две координаты в горизонтальной системе
        return Horizontal(*self._sub_(other))

    def __mul__(self, other):  # умножаем две координаты в горизонтальной системе
        return Horizontal(*self._mul_(other))
