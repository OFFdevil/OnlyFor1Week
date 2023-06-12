from unittest import TestCase

from math import atan2, cos, radians, sin

from geometry.equatorial import Equatorial
from geometry.horizontal import Horizontal
from tests.double_testcase import DoubleTestCase
from utility import foreach


class EquatorialToHorizontalTest(DoubleTestCase):
    @foreach("l", range(-90, 90, 8))
    def test_conversation_bijection(self, l):
        equ = set()
        hor = set()
        for a in range(-180, 180, 4):
            for d in range(-89, 89, 4):
                e = Equatorial(a, d)
                h = e.to_horizontal_with_latitude(l)
                equ.add(e)
                hor.add(h)
        self.assertEqual(len(equ), len(hor))


class HorizontalToPointTest(DoubleTestCase):
    @foreach("a", range(-180, 180))
    @foreach("h", range(-90, 90))
    def test_conversation(self, a, h):
        p = Horizontal(a, h).to_point()
        self.assertEqual(cos(radians(h)) * cos(radians(-a)), p.x, epsilon=self.EPS)
        self.assertEqual(cos(radians(h)) * sin(radians(-a)), p.y, epsilon=self.EPS)
        self.assertEqual(sin(radians(h)), p.z, epsilon=self.EPS)
