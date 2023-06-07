from math import cos, sin

import datetime
import jdcal


class FirstEquatorialToHorizontal:  # перевод из первой экваториальной в горизонтальную
    '''https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D1%82%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D0%BA%D0%BE%D0%BE%D1%80%D0%B4%D0%B8%D0%BD%D0%B0%D1%82'''

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
    @staticmethod
    def get_star_hour(longitude, date_time: datetime.datetime):
        d = StarTimeHelper.get_julian_day(date_time)
        t = d / 36525
        hours = (280.46061837 + 360.98564736629 * d + 0.000388 * (t ** 2) + longitude) % 360 / 15
        return hours

    @staticmethod
    def get_julian_day(dt: datetime): #передаем в функцию дату
        day = sum(jdcal.gcal2jd(dt.year, dt.month, dt.day)) #gcal2jd - перевод из григорианской в юлианскую
        day += dt.hour / 24
        day += dt.minute / 24 / 60
        day += dt.second / 24 / 60 / 60
        day += dt.microsecond / 24 / 60 / 60 / 1000000
        return day


class StarTime:
    @staticmethod
    def from_local(longitude: float, local: datetime):
        return StarTime(StarTimeHelper.get_star_hour(longitude, local))

    def __init__(self, hours: int):
        self._hours = hours

    @property
    def total_hours(self):
        return self._hours

    @property
    def total_minutes(self):
        return self.total_hours * 60

    @property
    def total_seconds(self):
        return self.total_minutes * 60

    @property
    def total_degree(self):
        return self.total_hours * 15
