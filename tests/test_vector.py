from unittest import main
from geometry.vector import Vector
from tests.double_testcase import DoubleTestCase


class VectorTest(DoubleTestCase):
    def setUp(self):
        self.a = Vector(1, 2, 3)
        self.b = Vector(4, 5, 6)
        self.m = [Vector(2, 0, 0), Vector(0, 2, 0), Vector(0, 0, 2)]

    def test_scalar_mul(self):
        expected = 4 + 10 + 18
        self.assertEqual(self.a.scalar_mul(self.b), expected)

    def test_vector_mul(self):
        n = self.a.vector_mul(self.b)
        self.assertEqual(n.scalar_mul(self.a), 0)
        self.assertEqual(n.scalar_mul(self.b), 0)

    def test_rmul_to_matrix(self):
        self.assertEqual(self.a.rmul_to_matrix(self.m), self.a * 2)

    def test_project_to(self):
        p = self.a.project_to(Vector(0, 0, 1))
        self.assertEqual(p, Vector(self.a.x, self.a.y, 0))

    def test_add(self):
        s = self.a + self.b
        self.assertEqual(s.x, self.a.x + self.b.x)
        self.assertEqual(s.y, self.a.y + self.b.y)
        self.assertEqual(s.z, self.a.z + self.b.z)

    def test_sub(self):
        s = self.a - self.b
        self.assertEqual(s.x, self.a.x - self.b.x)
        self.assertEqual(s.y, self.a.y - self.b.y)
        self.assertEqual(s.z, self.a.z - self.b.z)

    def test_mul(self):
        s = self.a * 7
        self.assertEqual(s.x, 7)
        self.assertEqual(s.y, 14)
        self.assertEqual(s.z, 21)


if __name__ == "__main__":
    main()
