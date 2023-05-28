import unittest
from vectors.vector import Vector


class VectorShould_CorrectCreated(unittest.TestCase):
    def test_creation(self):  # проверили, как программа отреагирует
        # на данный ввод
        x = 2
        y = 3
        z = 4
        v = Vector(x, y, z)
        self.assertEqual(v.x, x)
        self.assertEqual(v.y, y)
        self.assertEqual(v.z, z)

    def test_two(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
