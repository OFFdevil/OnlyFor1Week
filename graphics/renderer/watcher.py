import datetime

from geometry.avector import Horizontal
from geometry.sky_math import StarTime
from graphics.renderer.camera import Camera


class Watcher(Camera):
    def __init__(self, position: Horizontal, local_time: datetime, camera: Camera):
        # функция создает объект наблюдатель.
        # имеет координаты позиции, локальное и звездное время
        # рассчитываются на основании координат позиции и локального времени
        super().__init__(camera.sight_radius, camera.sight_vector)
        self._position = position
        self._local_time = local_time
        self._star_time = StarTime.from_local(position.alpha, local_time)  # вычисляем звездное время
        # if latitude == 90 or latitude == -90:
        # latitude += 1e-9

    @property
    def local_time(self):
        return self._local_time

    @local_time.setter
    def local_time(self, value: datetime):  # делает пересчет, когда
        # свойству local_time присваивается новое значение
        self._local_time = value
        self._star_time = StarTime.from_local(self.position.alpha, self.local_time)

    @property
    def star_time(self) -> StarTime:
        return self._star_time

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Horizontal):
        self._position = Horizontal(value.alpha % 360, min(90, max(-90, value.delta)))
        # ограничения угла альфа от -90 до 90, приводит альфа от 0 до 360
        # берем остаток от деления на 360
        self._star_time = StarTime.from_local(self.position.alpha, self.local_time)
        # пересчет звездного времени в зависимости от обновленных координат

