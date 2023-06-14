from math import cos, radians, sin
from geometry.angle_helpers import to_0_360, to_m180_180, time_to_seconds, seconds_to_degree, \
    time_to_degree, dtime_to_degree
from tests.double_testcase import DoubleTestCase
from utility import foreach


class AngleHelpersTest(DoubleTestCase):
    @foreach("foo", [to_0_360, to_m180_180])
    @foreach("d", range(-720, 720, 16))
    def test_equal_conversation_foo(self, foo, d):
        pd = foo(d)
        self.assertEqual(cos(radians(d)), cos(radians(pd)), foo.__name__, self.EPS)
        self.assertEqual(sin(radians(d)), sin(radians(pd)), foo.__name__, self.EPS)

    def test_time_to_seconds(self):
        time = (12, 17, 11)
        self.assertEqual(time_to_seconds(*time), 12 * 3600 + 17 * 60 + 11)

    def test_seconds_to_degree(self):
        seconds = 1800
        self.assertEqual(seconds_to_degree(seconds), seconds * 15 / 3600)

    def test_time_to_degree(self):
        time = (12, 17, 11)
        self.assertEqual(time_to_degree(*time), (12 * 3600 + 17 * 60 + 11) / 3600 * 15)

    def test_dtime_to_degree(self):
        dtime = (-53, 11, 32)
        self.assertEqual(dtime_to_degree(*dtime), -(53 + 11 / 60 + 32 / 3600))
