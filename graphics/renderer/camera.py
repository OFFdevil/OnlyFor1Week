import datetime

import numpy

from geometry.avector import Horizontal


class Camera:
    def __init__(self, longitude, latitude, sight_radius, sight_vector: Horizontal):
        if latitude == 90 or latitude == -90:  # если широта=90 или широта=-90
            latitude += 1e-9  # к широте прибавили значение 10^-9 - чтобы
            # уменьшить вероятность ошибок
        self._sight_radius = sight_radius  # радиус обзора
        self._sight_vector = Horizontal(sight_vector.alpha, sight_vector.delta)
        # protected куда смотрим - направление взгляда
        if sight_vector.delta == 90 or sight_vector.delta == -90:
            sight_vector.delta += 1e-9  # погрешность
        self._longitude = longitude  # долгота
        self._latitude = latitude  # широта
        self._up_rotation = 0  # вращение вверх
        self._oy_vector = Horizontal(0, 0)
        self._update()

    def _update(self):  # обновляем значение
        self._oy_vector = (self._sight_vector + Horizontal(self.up_rotation, -90)).to_point()
        self._ox_vector = self._sight_vector.to_point().vector_mul(self._oy_vector)
        self._transformation_matrix = numpy.array(
            [list(self._ox_vector), list(self._oy_vector), list(self._sight_vector.to_point())])

    @property
    def latitude(self):  # возвращает широту в данной координате
        return self._latitude

    @property
    def longitude(self):  # возвращает долготу в данной координате
        return self._longitude

    @latitude.setter  # сеттер широты
    def latitude(self, latitude):
        self._latitude = min(90, max(-90, latitude))

    @longitude.setter  # сеттер долготы
    def longitude(self, longitude):
        self._longitude = longitude % 360

    @property
    def sight_radius(self):  # возвращает радиус обзора
        return self._sight_radius

    @sight_radius.setter
    def sight_radius(self, radius):  # сеттер - устанавливаем значение радиуса обзора
        self._sight_radius = radius

    @property
    def up_vector(self) -> Horizontal:  # функция вернет объект типа Horizontal
        return self._oy_vector

    @property
    def sight_vector(self):
        return self._sight_vector

    @sight_vector.setter
    def sight_vector(self, value: Horizontal):
        # TODO: подозрительно
        self._sight_vector = Horizontal(value.alpha % 360, min(max(value.delta, -90 + 1e-9), 90 - 1e-9))
        self._update()

    @property
    def up_rotation(self):
        return self._up_rotation

    @up_rotation.setter
    def up_rotation(self, value):
        self._up_rotation = value
        self._update()

    @property
    def transformation_matrix(self):
        return self._transformation_matrix

    def get_lst(self, date_time: datetime.datetime):  # узнаем звездное время -
        # это время, которое используется, чтобы узнать, на какой объект направлять телескоп,
        # чтобы увидеть нужный объект. lst - часовой угол точки весеннего равноденствия
        # для данного места
        d = self.get_julian_day(date_time)
        t = d / 36525  # юлианский век = 36525 дней, делим на это число, чтобы
        # узнать кол-во веков, которые прошли с j2000 - 1.01.2000 12:00:00
        hours = (280.46061837 + 360.98564736629 * d + 0.000388 * (t ** 2) + self._longitude) % 360 / 15
        # считаем кол-во часов, которые прошли с 0 часов UT1 ого же дня,
        # базируется на значении долготы камеры
        return hours

    @staticmethod
    def get_julian_day(date_time: datetime.datetime):
        dwhole = (
                367 * date_time.year -
                int(7 * (date_time.year + int((date_time.month + 9) / 12)) / 4) +
                int(275 * date_time.month / 9) +
                date_time.day - 730531.5
        )  # считаем целую часть юлианского дня, который соответствует данной дате и времени
        dfrac = (date_time.hour + date_time.minute / 60 + date_time.second / 3600) / 24
        # считаем дробную часть юлианского дня на основе времени суток (datetime)
        # показывает сколько времени прошло с 0:00 до данного момента
        return dwhole + dfrac
