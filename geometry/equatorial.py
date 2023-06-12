import math

from geometry.angle_helpers import to_0_360, to_cos_period_cutted
from geometry.horizontal import Horizontal
from geometry.nvector import NVector
from geometry.sky_math import FirstEquatorialToHorizontal, atan2


class Equatorial(NVector):
    def __init__(self, a, d):  # инициализация координат в экваториальной системе
        super().__init__((to_0_360(a), to_cos_period_cutted(d)))

    def apply_time_rotation(self, star_time_degree):  # позволяет обновлять восхождение
        # для наблюдаемых объектов в зависимости от времени наблюдения.
        return Equatorial(self.a + star_time_degree, self.d)

    def to_horizontal_with_latitude(self, h) -> Horizontal:  # преобразует координаты из экваториальной
        # в горизонтальную, используя значение звездного времени (звездные градусы)
        # и высоту наблюдателя (градусы)
        f, t, d = map(math.radians, (h, *self))

        cosz = FirstEquatorialToHorizontal.cosz(f, d, t)
        sina_sinz = FirstEquatorialToHorizontal.siza_sinz(d, t)
        cosa_sinz = FirstEquatorialToHorizontal.cosa_sinz(f, d, t)

        if abs(cosz) > 1:
            cosz = 1 if cosz > 0 else -1
        sinz = math.sqrt(1 - cosz ** 2)
        if sinz == 0:
            return Horizontal(0, 90)
        sina = sina_sinz / sinz
        cosa = cosa_sinz / sinz
        a = atan2(sina, cosa)
        d = atan2(sinz, cosz)
        return Horizontal(*map(math.degrees, (a, math.pi / 2 - d)))

    def to_horizontal_with_time(self, star_time_degree, h) -> Horizontal:
        return self.apply_time_rotation(star_time_degree).to_horizontal_with_latitude(h)
        # возвращает объект в горизонтальной системе координат в зависимости
        # от значения звездного времени

    @property
    def a(self):  # получаем значение прямого восхождения
        return self[0]

    @property
    def d(self):  # получаем значение склонения
        return self[1]

    def __add__(self, other):  # складываем две координаты в экваториальной системе
        return Equatorial(*self._add_(other))

    def __sub__(self, other):  # вычитаем две координаты в экваториальной системе
        return self + other*(-1)

    def __mul__(self, other):  # умножаем две координаты в экваториальной системе
        return Equatorial(*self._mul_(other))
