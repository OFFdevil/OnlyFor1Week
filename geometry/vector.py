from math import sqrt, acos

import numpy


class Vector:  # точка в пространстве
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):  #геттер
        return self._x

    @property
    def y(self):  # геттер
        return self._y

    @property
    def z(self):  # геттер
        return self._z

    @property
    def length(self):  # возвращает длину вектора
        return sqrt(self.scalar_mul(self))

    def angle_to(self, other):  # угол между векторами
        d = other - self
        if self.length == 0 or other.length == 0:
            return 0
        return acos((self.length ** 2 + other.length ** 2 - d.length ** 2) / 2 / self.length / other.length)

    def scalar_mul(self, other):  # cкалярное произведение
        return self.x * other.x + self.y * other.y + self.z * other.z

    def vector_mul(self, other):  # функция вычисляет векторное произведение
        x = numpy.linalg.det([[self.y, self.z], [other.y, other.z]])
        y = -numpy.linalg.det([[self.x, self.z], [other.x, other.z]])
        z = numpy.linalg.det([[self.x, self.y], [other.x, other.y]])
        return Vector(x, y, z)

    def mul_to_matrix(self, matrix):  # выводит произведение вектора на matrix
        return Vector(*numpy.matmul(list(self), matrix))

    def rmul_to_matrix(self, matrix):  # выводит произведение matrix на вектор
        return Vector(*numpy.matmul(matrix, list(self)))

    def change_basis(self, x, y, z):  # переход от одного базиса к другому
        return self.rmul_to_matrix(numpy.array([list(x), list(y), list(z)]))

    def project_to(self, plane_normal_vector):  # вычисление проекции
        sqr = plane_normal_vector.scalar_mul(plane_normal_vector)
        mul = self.scalar_mul(plane_normal_vector)
        t = -mul / sqr
        return self + t * plane_normal_vector

    def __add__(self, other):  # сложение векторов
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):  # скаляр произведение
        return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self * other

    def __sub__(self, other):  # разность векторов
        return self + other * -1

    def __iter__(self):
        yield self.x  # yield - аналог return, только возвращает генератор
        yield self.y
        yield self.z

    def __next__(self):
        yield self.x
        yield self.y
        yield self.z

    def __str__(self):  # выводит вектор в заданном формате
        return "({}, {}, {})".format(*self)  # * перед аргументом - аналог (self.x, self.y, self.z)

    def __eq__(self, other):  # проверяет равенство
        return self.x == other.x and self.y == other.y and self.z == other.z
