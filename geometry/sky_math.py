from functools import lru_cache
from math import cos as mcos, sin as msin, atan2 as matan2, floor
import datetime
import jdcal


def sign(n):
    return -1 if n < 0 else (0 if n == 0 else 1)


@lru_cache(128)
def cos(a):
    return mcos(a)


@lru_cache(128)
def sin(a):
    return msin(a)


@lru_cache(128)
def atan2(y, x):
    return matan2(y, x)


class FirstEquatorialToHorizontal:  # перевод из первой экваториальной в горизонтальную
    """https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D1%82%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0
    %D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D0%BA%D0%BE%D0%BE%D1%80%D0%B4%D0%B8%D0%BD%D0%B0%D1%82"""

    # далее вспомогательные функции для перехода из первой экваториальной в горизонтальную(формулы с вики)
    # f-широта
    # t- часовой угол светила
    # d-склонение светила
    # z-Зенитное расстояние z
    # a-Азимут светила
    @staticmethod
    def cosz(f, d, t):
        return sin(f) * sin(d) + cos(d) * cos(f) * cos(t)

    @staticmethod
    def siza_sinz(d, t):
        return cos(d) * sin(t)

    @staticmethod
    def cosa_sinz(f, d, t):
        return -cos(f) * sin(d) + sin(f) * cos(d) * cos(t)


class StarTimeHelper:
    """http://www.jgiesen.de/astro/astroJS/siderealClock/sidClock.js"""

    # определяем звездное время в часах для определенной даты и местности
    @staticmethod
    def get_star_hour(longitude, dt: datetime):
        """see: GM_Sidereal_Time, LM_Sidereal_Time"""
        jd = StarTimeHelper.get_julian_day(dt)
        MJD = jd - 2400000.5
        MJD0 = floor(MJD)
        ut = (MJD - MJD0) * 24.0
        t_eph = (MJD0 - 51544.5) / 36525.0
        GM0ST = 6.697374558 + 1.0027379093 * ut + (
                8640184.812866 + (0.093104 - 0.0000062 * t_eph) * t_eph) * t_eph / 3600.0
        return GM0ST + longitude / 15

    # представляет дату в системе юлианского календаря из грегорианского
    @staticmethod
    def get_julian_day(dt: datetime):
        day = sum(jdcal.gcal2jd(dt.year, dt.month, dt.day))
        day += dt.hour / 24
        day += dt.minute / 24 / 60
        day += dt.second / 24 / 60 / 60
        day += dt.microsecond / 24 / 60 / 60 / 1000000
        return day
