from unittest import main
from math import cos, radians, sin
from geometry.equatorial import Equatorial
from geometry.horizontal import Horizontal
from tests.double_testcase import DoubleTestCase
from utility import foreach


class HorizontalTest(DoubleTestCase):
    def setUp(self):
        self.v = Horizontal(3, 4)
        self.a = Horizontal(1, 2)

    @foreach("a", range(-360, 360, 1))
    @foreach("d", range(-90, 90, 1))
    def test_init(self, a, d):
        v = Equatorial(a, d)
        self.assertEqual(cos(radians(a)), cos(radians(v.a)), epsilon=HorizontalTest.EPS)
        self.assertEqual(sin(radians(a)), sin(radians(v.a)), epsilon=HorizontalTest.EPS)
        self.assertEqual(sin(radians(d)), sin(radians(v.d)), epsilon=HorizontalTest.EPS)
        self.assertEqual(sin(radians(d)), sin(radians(v.d)), epsilon=HorizontalTest.EPS)

    def test_add(self):
        s = self.v + self.a
        self.assertEqual(s.a, self.a.a + self.v.a)
        self.assertEqual(s.h, self.a.h + self.v.h)

    def test_sub(self):
        s = self.a - self.a
        self.assertEqual(s.a, self.a.a - self.a.a, str(s))
        self.assertEqual(s.h, self.a.h - self.a.h, str(s))

    def test_mul(self):
        s = self.v * 7
        self.assertEqual(s.a, 21)
        self.assertEqual(s.h, 28)

    @foreach("a0", range(-360, 360, 32))
    @foreach("h0", range(-90, 90, 16))
    @foreach("a1", range(-360, 360, 32))
    @foreach("h1", range(-90, 90, 16))
    def test_cos_to(self, a0, h0, a1, h1):
        a = Horizontal(a0, h0)
        b = Horizontal(a1, h1)
        pa = a.to_point()
        pb = b.to_point()
        expected = -((pa - pb).length ** 2 - pa.length ** 2 - pb.length ** 2) / (2 * pa.length * pb.length)
        self.assertEqual(a.cos_to(b), expected, epsilon=self.EPS)


if __name__ == "__main__":
    main()
