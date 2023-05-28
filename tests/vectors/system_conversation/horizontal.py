import unittest
from math import sqrt

from tests.vectors.utility.for_decorator import for_range
from vectors.vector import Vector, Horizontal


class HorizontalConversationTest(unittest.TestCase):
    def setUp(self):
        self.epsilon = 0.0001

    @staticmethod
    def distance(a: Horizontal, b: Horizontal):  # вычисление раст. между двумя векторами в полярной системе координат
        dh = (a.h - b.h) ** 2
        da = (a.a - b.a) ** 2
        dr = (a.r - b.r) ** 2
        return sqrt(da + dh + dr)

    @for_range('h', range(-180, 180))  # перебор по парам a h и вызывов ф-и тестирующей
    @for_range('a', range(-90, 90))
    def qtest_save_radius_as_length(self, h, a):  # запускаем функцию от a,h
        hor = Horizontal(h, a, 1000)  # создаем по данным а,h вектор в полярных коорд
        v = Vector.from_horizontal(
            *hor)  # *hor - в функцию передали весь кортеж из трех аргументов. Переводим в декартову
        self.assertLess(abs(1000 - v.length), self.epsilon,
                        str(h) + ' ' + str(a))  # проверяем, что радиус в полярной = длина в декартовой

    @for_range('h', range(-180, 180))  # перебор по парам a h и вызывов ф-и тестирующей
    @for_range('a', range(-90, 90))
    def qtest_save_length_as_radius(self, h, a):  # запускаем функцию от a,h
        hor = Horizontal(h, a, 1000)  # создаем по данным а,h вектор в полярных коорд
        v = Vector.from_horizontal(
            *hor)  # *hor - в функцию передали весь кортеж из трех аргументов. Переводим в декартову
        hor2 = v.to_horizontal()  # перевели обратно в полярные
        self.assertLess(abs(v.length - hor2.r), self.epsilon,
                        str(h) + ' ' + str(a))  # проверяем что длина в декартовой = радиус в полярной

    @for_range('h', range(-180, 180))  # перебор по парам a h и вызывов ф-и тестирующей
    @for_range('a', range(-90, 90))
    def test_correct_reconversion(self, h, a):
        hor = Horizontal(h, a, 5)  # создаем по данным а,h вектор в полярных коорд
        v = Vector.from_horizontal(
            *hor)  # *hor - в функцию передали весь кортеж из трех аргументов. Переводим в декартову
        hor2 = v.to_horizontal()  # переводим обратно в полярные
        self.assertLess(self.distance(hor2, hor), self.epsilon,
                        str(hor) + '->' + str(hor2))  # проверяем, что расст -> 0


if __name__ == '__main__':
    unittest.main()
