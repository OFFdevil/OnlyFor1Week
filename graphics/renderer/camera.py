import numpy

from geometry.horizontal import Horizontal


class Camera:
    def __init__(self, see: Horizontal, radius):
        self._radius = radius  # радиус обзора
        self._see = Horizontal(see.a, see.h)
        # protected куда смотрим - направление взгляда
        if see.h == 90 or see.h == -90:
            see.h += 1e-9  # погрешность
        self._up_rotation = 0  # вращение вверх
        self._oy = Horizontal(0, 0)
        self._update()

    def _update(self):  # обновляем значение
        self._oy = (self._see + Horizontal(self.up_rotation, -90)).to_point()
        self._ox_vector = self._see.to_point().vector_mul(self._oy)
        self._transformation_matrix = numpy.array(
            [list(self._ox_vector), list(self._oy), list(self._see.to_point())])

    @property
    def eye_radius(self):  # возвращает радиус обзора
        return self._radius

    @eye_radius.setter
    def eye_radius(self, radius):  # сеттер - устанавливаем значение радиуса обзора
        self._radius = radius

    @property
    def up(self) -> Horizontal:  # функция вернет объект типа Horizontal
        return self._oy

    @property
    def see(self):
        return self._see

    @see.setter
    def see(self, value: Horizontal):
        # TODO: подозрительно
        self._see = Horizontal(value.a % 360, min(max(value.h, -90 + 1e-9), 90 - 1e-9))
        self._update()

    @property
    def up_rotation(self):
        return self._up_rotation

    @up_rotation.setter
    def up_rotation(self, value):
        self._up_rotation = value % 360
        self._update()

    @property
    def transformation_matrix(self):
        return self._transformation_matrix
