from unittest import TestCase
from unittest import main
from math import cos, radians, sin
from geometry.equatorial import Equatorial
from tests.double_testcase import DoubleTestCase
from utility import foreach


class EquatorialTest(DoubleTestCase):
    def setUp(self):
        self.v = Equatorial(3, 4)
        self.a = Equatorial(1, 2)

    @foreach("a", range(-360, 360, 1))
    @foreach("d", range(-90, 90, 1))
    def test_init(self, a, d):
        v = Equatorial(a, d)
        self.assertEqual(cos(radians(a)), cos(radians(v.a)), epsilon=EquatorialTest.EPS)
        self.assertEqual(sin(radians(a)), sin(radians(v.a)), epsilon=EquatorialTest.EPS)
        self.assertEqual(sin(radians(d)), sin(radians(v.d)), epsilon=EquatorialTest.EPS)
        self.assertEqual(sin(radians(d)), sin(radians(v.d)), epsilon=EquatorialTest.EPS)

    def test_add(self):
        s = self.v + self.a
        self.assertEqual(s.a, self.a.a + self.v.a)
        self.assertEqual(s.d, self.a.d + self.v.d)

    def test_sub(self):
        s = self.a - self.a
        self.assertEqual(s.a, self.a.a - self.a.a, str(s))
        self.assertEqual(s.d, self.a.d - self.a.d, str(s))

    def test_mul(self):
        s = self.v * 7
        self.assertEqual(s.a, 21)
        self.assertEqual(s.d, 28)

    @foreach("s", range(0, 360, 8))
    @foreach("a", range(-180, 180, 16))
    @foreach("d", range(-90, 90, 2))
    def test_apply_time_rotation(self, s, a, d):
        v = Equatorial(a, d).apply_time_rotation(s)
        a += s
        self.assertEqual(cos(radians(a)), cos(radians(v.a)), epsilon=EquatorialTest.EPS)
        self.assertEqual(sin(radians(a)), sin(radians(v.a)), epsilon=EquatorialTest.EPS)
        self.assertEqual(sin(radians(d)), sin(radians(v.d)), epsilon=EquatorialTest.EPS)
        self.assertEqual(sin(radians(d)), sin(radians(v.d)), epsilon=EquatorialTest.EPS)


if __name__ == "__main__":
    main()
