from math import cos, sin, pi, atan2, sqrt
from collections import namedtuple
from vectors._base import VectorBase
from vectors.convetation import to_radian, to_degree

Horizontal = namedtuple("Horizontal", ["h", "a", "r"])


class Vector(VectorBase):
    # TODO: implement
    @staticmethod
    def from_first_equatorial(d, t, radius=1): #перевод из первой формы экваториальной системы
        raise NotImplementedError("TODO")

    @staticmethod
    def from_second_equatorial(d, a, radius=1): ##перевод из второй формы экваториальной системы
        raise NotImplementedError("TODO")

    @staticmethod
    def from_horizontal(h, a, radius=1):  #перевод из полярной в декартову систему
        a = to_radian(a)
        h = to_radian(h)
        return Vector(cos(-a) * cos(h), cos(h) * sin(-a), sin(h)) * radius

    def __init__(self, x, y, z):
        super().__init__(x, y, z)

    def to_first_equatorial(self):
        raise NotImplementedError("TODO")

    def to_second_equatorial(self):
        raise NotImplementedError("TODO")

    def to_horizontal(self):
        return Horizontal(to_degree(atan2(self.z, sqrt(self.x ** 2 + self.y ** 2))), to_degree(-atan2(self.y, self.x)),
                          self.length)

    def __add__(self, other):
        return Vector(other.x + self.x, other.y + self.y, other.z + self.z)

    def __mul__(self, other): #произведение вектора на число
        if isinstance(other, float) or isinstance(other, int):
            return Vector(self.x * other, self.y * other, self.z * other)
        else:
            raise NotImplementedError("Not supported")

    def __invert__(self):
        return self * (-1)

    def __sub__(self, other):
        return self + other * (-1)
