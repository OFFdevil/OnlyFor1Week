import math
from math import sin, cos
from geometry.vector import Vector
from geometry.sky_math import FirstEquatorialToHorizontal


class AngleVector:
    def __init__(self, alpha, delta):
        self.alpha = alpha
        self.delta = delta

    def length(self):  # длина вектора
        return math.sqrt(self.alpha ** 2 + self.delta ** 2)

    def __str__(self):
        return "({}, {})".format(self.alpha, self.delta)

    def __eq__(self, other):  # проверка двух векторов на равенство
        av = AngleVector(self.alpha - other.alpha, self.delta - other.delta)
        return av < 1e-5


class Equatorial(AngleVector):  # в экваториальной системе координат
    def __init__(self, a, d):
        super().__init__(a, d)

    def apply_time(self, sidereal_time):  # ?
        return Equatorial(self.alpha + sidereal_time, self.delta)

    def to_horizontal_system(self, latitude, sidereal_time):  # перевод из экваториальной в горизонтальную
        timed = self.apply_time(sidereal_time)
        d = math.radians(timed.delta)
        t = math.radians(timed.alpha)
        f = math.radians(latitude)
        cosz = FirstEquatorialToHorizontal.cosz(f, d, t)
        sina_sinz = FirstEquatorialToHorizontal.siza_sinz(d, t)
        cosa_sinz = FirstEquatorialToHorizontal.cosa_sinz(f, d, t)

        sinz = math.sqrt(1 - cosz ** 2)
        if sinz == 0:
            return Horizontal(0, 90)

        sina = sina_sinz / sinz
        cosa = cosa_sinz / sinz
        a = math.atan2(sina, cosa)
        d = math.atan2(sinz, cosz)
        return Horizontal.star_compatible(math.degrees(a), 90 - math.degrees(d))

    def __add__(self, other):  # сложение
        return Equatorial(self.alpha + other.alpha, self.delta + other.delta)

    def __sub__(self, other):  # вычитание
        return Equatorial(self.alpha - other.alpha, self.delta - other.delta)


class Horizontal(AngleVector):  # вектор в горизонтальной системе координат

    def __init__(self, a, d):
        super().__init__(a, d)

    @staticmethod
    def star_compatible(a, d):
        return Horizontal((a + 360) % 360, d)

    def to_point(self, radius=1) -> Vector:  # перевод в декартову систему координат
        a = math.radians(-self.alpha)
        h = math.radians(self.delta)
        z = radius * math.sin(h)
        r = math.sqrt(radius ** 2 - z ** 2)
        x = r * math.cos(a)
        y = r * math.sin(a)
        return Vector(x, y, z)

    def angle_to(self, other_point):  # угол между векторами
        # переводим в декартову
        return math.degrees(self.to_point().angle_to(other_point.to_point()))

    def __add__(self, other):  # сумма векторов
        return Horizontal(self.alpha + other.alpha, self.delta + other.delta)

    def __sub__(self, other):  # разность векторов
        return Horizontal(self.alpha - other.alpha, self.delta - other.delta)
