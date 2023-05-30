import math

from geometry.point import Point

EPS = 1e-9


def almost_equal(a: float, b: float) -> bool:
    return abs(a - b) < EPS


class Base:
    def __init__(self, alpha, delta):
        self.alpha = alpha
        self.delta = delta

    def __str__(self):  # выводит в заданном формате
        return "alpha: {}, delta: {}".format(self.alpha, self.delta)

    def __eq__(self, other):  # проверяет на равенство
        return almost_equal(self.alpha, other.alpha) and almost_equal(self.delta, other.delta)


class SecondEquatorial(Base):  # вторая экваториальная система координат. Наследуемся от Base
    def __init__(self, a, d):  # конструктор
        super().__init__(a, d)

    def _to_first_equatorial_system(self, sidereal_time):
        """Conversion from second equatorial coordinate system to first"""
        return Base(self.alpha + sidereal_time, self.delta)

    def to_horizontal_system(self, latitude, sidereal_time):
        """Conversion from second equatorial coordinate system to horizontal system"""
        first_equat_sys_point = self._to_first_equatorial_system(sidereal_time)
        delta = math.radians(first_equat_sys_point.delta)
        t = math.radians(first_equat_sys_point.alpha)
        fi = math.radians(latitude)
        cos_z = (
                math.sin(delta) * math.sin(fi) +
                math.cos(delta) * math.cos(fi) * math.cos(t)
        )
        # z <= 90 degrees, so cos(z) >= 0 and sin(z) >= 0
        sin_z = math.sqrt(1 - cos_z ** 2)
        if sin_z == 0:
            return Horizontal(0, 90)
        sin_a = math.cos(delta) * math.sin(t) / sin_z
        cos_a = (
                        -math.cos(fi) * math.sin(delta) +
                        math.sin(fi) * math.cos(delta) * math.cos(t)
                ) / sin_z
        a = math.atan2(sin_a, cos_a)
        z = math.atan2(sin_z, cos_z)
        return Horizontal((math.degrees(a) + 360) % 360, 90 - math.degrees(z))


class Horizontal(Base):  # декартова система координат
    def __init__(self, a, d):
        super().__init__(a, d)

    def to_point(self, radius=1) -> Point:  # фнукция принимает вектор, возвращает его как Point
        a = math.radians(-self.alpha)
        h = math.radians(self.delta)
        z = radius * math.sin(h)
        r = math.sqrt(radius ** 2 - z ** 2)
        x = r * math.cos(a)
        y = r * math.sin(a)
        return Point(x, y, z)

    def __add__(self, other):  #сложение
        return Horizontal(self.alpha + other.alpha, self.delta + other.delta)

    def angle_to(self, other_point):  # угол между векторами в градусах(сначала переводим в оба к типу Point)
        return math.degrees(self.to_point().angle_to(other_point.to_point()))
