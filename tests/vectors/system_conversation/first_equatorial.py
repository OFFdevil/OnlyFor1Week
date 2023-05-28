import unittest
from tests.vectors.utility.for_decorator import for_range
from vectors.vector import Vector, Horizontal


class FirstEquatorialConversationTest(unittest.TestCase):
    #тестирование перевода из/в первую экваториальную систему координат
    def setUp(self):
        self.epsilon = 0.001

    @staticmethod #вычисление расстояния  между векторами в полярной системе координат
    def distance(a: Horizontal, b: Horizontal):
        return max(abs(a.h - b.h), abs(a.a - b.a))

    @for_range('h', range(-90, 90))
    @for_range('a', range(-180, 180))
    def test_save_radius_as_length(self, h, a):
        hor = Horizontal(h, a, 1000)
        v = Vector.from_horizontal(*hor)
        self.assertLess(abs(1000 - v.length), self.epsilon, str(h) + ' ' + str(a))

    @for_range('h', range(-90, 90))
    @for_range('a', range(-180, 180))
    def test_save_length_as_radius(self, h, a):
        hor = Horizontal(h, a, 1000)
        v = Vector.from_horizontal(*hor)
        hor2 = v.to_horizontal()
        self.assertLess(abs(v.length - hor2.r), self.epsilon, str(h) + ' ' + str(a))

    @for_range('h', range(-90, 90))
    @for_range('a', range(-180, 180))
    def test_correct_reconversion(self, h, a):
        hor = Horizontal(h, a, 5)
        v = Vector.from_horizontal(*hor)
        hor2 = v.to_horizontal()
        self.assertLess(self.distance(hor2, hor), self.epsilon, str(hor) + '->' + str(hor2))


if __name__ == '__main__':
    unittest.main()
