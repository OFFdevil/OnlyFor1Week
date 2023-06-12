from math import sqrt
from geometry.nvector import NVector


class Vector(NVector):
    def __init__(self, x, y, z):
        super().__init__((x, y, z))

    def scalar_mul(self, other):  # скалярное произведение
        return self.x * other.x + self.y * other.y + self.z * other.z

    def vector_mul(self, other):  # векторное произведение
        p, q, r = self
        m, n, t = other
        x = q * t - n * r
        y = -(p * t - m * r)
        z = (p * n - q * m)
        return Vector(x, y, z)

    def rmul_to_matrix(self, matrix):  # умножение вектора на матрицу
        return Vector(*(self.scalar_mul(row) for row in matrix))

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
