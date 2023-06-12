from unittest import TestCase
from unittest import main
from geometry.nvector import NVector
from tests.double_testcase import DoubleTestCase


class NVectorTest(DoubleTestCase):
    def setUp(self):
        self.v = NVector((3, 4, 5))
        self.a = NVector((1, 2))
        self.b = NVector((3, 4))
        self.eb = NVector((3, 4))

    def test_rank(self):
        self.assertEqual(self.v.rank, 3)

    def test_length(self):
        self.assertEqual(self.b.length, 5)

    def test_indexation(self):
        self.assertEqual(self.v[0], 3)
        self.assertEqual(self.v[1], 4)
        self.assertEqual(self.v[2], 5)

    def test_iteration(self):
        self.assertEqual(tuple([*self.v]), (3, 4, 5))

    def test_add(self):
        s = self.a._add_(self.b)
        self.assertEqual(s[0], 4)
        self.assertEqual(s[1], 6)

    def test_mul(self):
        s = self.a._mul_(7)
        self.assertEqual(s[0], 7)
        self.assertEqual(s[1], 14)

    def test_sub(self):
        s = self.a._sub_(self.b)
        self.assertEqual(s[0], -2)
        self.assertEqual(s[1], -2)

    def test_str(self):
        self.assertEqual(str(self.v), "(3, 4, 5)")

    def test_hash(self):
        self.assertEqual(hash(self.b), hash(self.eb))

    def test_equal(self):
        self.assertEqual(self.b, self.eb)


if __name__ == "__main__":
    main()
