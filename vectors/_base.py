from math import sqrt

from vectors.vector import Vector


class VectorBase:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self): # х-овая координата вектора
        return self._x

    @property
    def y(self): # у-овая координата вектора
        return self._y

    @property
    def z(self): # z-овая координата вектора
        return self._z

    @property
    def length(self): # посчитали длину вектора по формуле
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __len__(self): # возвращает длину вектора
        return self.length

    def __str__(self): # возвращает координаты вектора в виде строки
        return '(' + self.x + ', ' + self.y + ', ' + self.z + ')'

    def __eq__(self, other): # проверка двух векторов на равенство
        if not isinstance(other, Vector): # проверка принадлежности other к Vector
            return False
        return self.x == other.x and self.y == other.y and self.z == other.y
