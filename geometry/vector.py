from math import sqrt, acos

import numpy

from geometry.nvector import NVector


class Vector(NVector):
    def __init__(self, x, y, z):
        super().__init__((x, y, z))

    @property
    def length(self):  # длина вектора
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

    # геттеры
    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    def __add__(self, other):  # сложение векторов
        return Vector(*self._add_(other))

    def __mul__(self, other):  # скаляр произведение
        return Vector(*self._mul_(other))

    def __rmul__(self, other):
        return Vector(*self._mul_(other))

    def __sub__(self, other):  # разность векторов
        return Vector(*self._sub_(other))

    def __str__(self):  # выводит вектор в заданном формате
        return "({}, {}, {})".format(*self)  # * перед аргументом - перечисляем все поля

    def __eq__(self, other):  # проверяет равенство
        return self.x == other.x and self.y == other.y and self.z == other.z
