import math
from math import sin, cos
from geometry.vector import Vector


class AngleVector:
    def __init__(self, alpha, delta):
        self._alpha = alpha
        self._delta = delta

    @property  # геттер
    def alpha(self):
        return self._alpha

    @property  # геттер
    def delta(self):
        return self._delta

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

    def apply_time(self, sidereal_time): #?
        return Equatorial(self.alpha + sidereal_time, self.delta)

    def to_horizontal_system(self, latitude, sidereal_time): #перевод из экваториальной в горизонтальную
        timed = self.apply_time(sidereal_time)
        delta = math.radians(timed.delta)
        t = math.radians(timed.alpha)
        phi = math.radians(latitude)
        cos_z = sin(phi) * sin(delta) + cos(delta) * cos(phi) * cos(t)
        sin_z = math.sqrt(1 - cos_z ** 2)
        if sin_z == 0:
            return Horizontal(0, 90)
        sin_a = cos(delta) * sin(t) / sin_z
        cos_a = (-cos(phi) * sin(delta) + sin(phi) * cos(delta) * math.cos(t)) / sin_z
        a = math.atan2(sin_a, cos_a)
        z = math.atan2(sin_z, cos_z)
        # TODO: create method to_first_period
        return Horizontal((math.degrees(a) + 360) % 360, 90 - math.degrees(z))

    def __add__(self, other):  # сложение
        return Equatorial(self.alpha + other.alpha, self.delta + other.delta)

    def __sub__(self, other):  # вычитание
        return Equatorial(self.alpha - other.alpha, self.delta - other.delta)


class Horizontal(AngleVector):  # вектор в горизонтальной системе координат
    def __init__(self, a, d):  # инициализируем вектор
        super().__init__(a, d)

    def to_point(self, radius=1) -> Vector:  # перевод в декартову систему координат
        a = math.radians(-self.alpha)
        h = math.radians(self.delta)
        z = radius * math.sin(h)
        r = math.sqrt(radius ** 2 - z ** 2)
        x = r * math.cos(a)
        y = r * math.sin(a)
        return Vector(x, y, z)

    def angle_to(self, other_point):  # угол между векторами
        #переводим в декартову
        return math.degrees(self.to_point().angle_to(other_point.to_point()))

    def __add__(self, other):  # сумма векторов
        return Horizontal(self.alpha + other.alpha, self.delta + other.delta)

    def __sub__(self, other):  # разность векторов
        return Horizontal(self.alpha - other.alpha, self.delta - other.delta)
