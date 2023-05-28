import unittest

from vectors.vector import Vector


class VectorTest(unittest.TestCase):
    def setUp(self): #создаем два вектора а и b c заданными значениями
        self.a = Vector(100500, 100, 4)
        self.b = Vector(2, 100, 4)

    def test_sum(self): #тест функции суммы
        expected = Vector(self.a.x + self.b.x, self.a.y + self.b.y, self.a.z + self.b.z)
        self.assertEqual(self.a + self.b, expected)

    def test_mul_to_int(self): #тест умножения вектора на целое число
        m = 7
        expected = Vector(self.a.x * m, self.a.y * m, self.a.z * m)
        self.assertEqual(self.a * m, expected)

    def test_mul_to_float(self): #тест умножения вектора на дробное число
        m = 0.5
        expected = Vector(self.a.x * m, self.a.y * m, self.a.z * m)
        self.assertEqual(self.a * m, expected)

    def test_throws_when_incorrect_mul(self): #тест умножения на что-то иное(падает с тайп ерор)
        m = 'stuff'
        with self.assertRaises(TypeError):
            self.a * m

    def test_sub(self): #тест вычитание векторов
        expected = Vector(self.a.x - self.b.x, self.a.y - self.b.y, self.a.z - self.b.z)
        self.assertEqual(self.a - self.b, expected)


if __name__ == '__main__':
    unittest.main()
