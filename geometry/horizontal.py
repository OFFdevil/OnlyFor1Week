import math

from geometry.nvector import NVector
from geometry.vector import Vector


class Horizontal(NVector):
    @staticmethod
    def star_compatible(a, d):
        return Horizontal((a + 360) % 360, d)

    def __init__(self, a, d):
        super().__init__((a, d))

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
