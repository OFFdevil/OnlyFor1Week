import datetime
from stars.sky_math import StarTimeHelper

'''https://en.wikipedia.org/wiki/Sidereal_time'''


class StarTime:  # класс для работы со звездным временем - lst - куда надо направить телескоп
    # чтобы увидеть нужный объект (с помощью звездного времени вычисляют положение объекта на небе)
    @staticmethod
    def from_local(longitude: float, local: datetime):
        return StarTime(StarTimeHelper.get_star_hour(longitude, local))

    def __init__(self, hours: int):  # _hours - количество звездных часов
        self._hours = hours

    @property
    def total_hours(self):  # подсчет общего кол-ва звездных часов
        return self._hours

    @property
    def total_minutes(self):  # подсчет общего кол-ва звездных минут
        return self.total_hours * 60

    @property
    def total_seconds(self):  # подсчет общего кол-ва звездных секунд
        return self.total_minutes * 60

    @property
    def total_degree(self):  # возвращает общее кол-во звездных градусов, умножаем на 15
        # тк в одном звездном часе содержится 15 звездных градусов
        return self.total_hours * 15

    def __int__(self):  # возвращает целую часть общего количества звездных секунд
        return int(self.total_seconds)

    def __float__(self):  # возвращает общее количество звездных секунд
        # в виде числа с плавающей запятой
        return float(self.total_seconds)

    def __str__(self):  # возвращает строковое представление целой части
        # общего количества звездных секунд.
        return str(int(self))
