import math

from geometry.angle_helpers import to_0_360, to_cos_period_cutted
from geometry.nvector import NVector
from geometry.vector import Vector


class Horizontal(NVector):

    def __init__(self, a, h):  # TODO: все брать по модулю 360 и в -90 до 90 по умолчанию!!!!
        super().__init__((to_0_360(a), to_cos_period_cutted(h)))

    def to_point(self, radius=1) -> Vector:
        a = math.radians(-self.a)
        h = math.radians(self.h)
        z = radius * math.sin(h)
        r = math.sqrt(radius ** 2 - z ** 2)
        x = r * math.cos(a)
        y = r * math.sin(a)
        return Vector(x, y, z)

    def angle_to(self, other_point):
        return math.degrees(self.to_point().angle_to(other_point.to_point()))

    @property
    def a(self):
        return self[0]

    @property
    def h(self):
        return self[1]

    def __add__(self, other):
        return Horizontal(*self._add_(other))

    def __sub__(self, other):
        return Horizontal(*self._sub_(other))

    def __mul__(self, other):
        return Horizontal(*self._mul_(other))
