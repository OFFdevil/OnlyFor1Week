from collections import namedtuple
from math import sqrt, e, log, pi
from geometry.horizontal import Horizontal
from graphics.renderer.settings import Settings
from graphics.renderer.watcher import Watcher
from stars.star import Star


# функция считает искажение, которое возникает при съёмке с широкоугольной камеры (искажение рыбьего глаза) она
# вычисляет координаты точки на изображении с помощью формулы с использованием: dx, dy- координаты точки на плоском
# изображении, sight_radius - радиус обзора широкоугольной камеры, z - расстояние между плоскостью
# изображения и центром камеры
def fisheye_distortion(x, y, radius, z):
    r = radius * 10 / (1 - abs(z)) ** 2
    return x * r, y * r


# функция осуществляет шкалирование координат x, y на основе радиуса обзора
def scale_distortion(x, y, radius, z):
    return x * radius * 10, y * radius * 10


ProjectedStar = namedtuple('ProjectedStar', ['cx', 'cy', 'diameter', 'star'])


class Projector:
    def __init__(self, watcher: Watcher):
        super().__init__()
        self.settings = Settings()
        self.watcher = watcher
        self._distortion = fisheye_distortion
        self._objects = []
        self.centre = (0, 0)
        self._constellations = {}

    def project(self, stars: list) -> list:
        self._distortion = fisheye_distortion if self.settings.fisheye else scale_distortion

        self._objects.clear()
        self._constellations = {}
        for o in (self._apply_time_rotation(s) for s in stars):
            if o[1].constellation in self._constellations:
                current = self._constellations[o[1].constellation]
                self._constellations[o[1].constellation] = min(current, o, key=lambda s: s[1].magnitude)
            else:
                self._constellations[o[1].constellation] = o
            p = self.project_star(*o)
            if p is not None:
                self._objects.append(p)

        return self._objects

    def find_star(self, screenX, screenY, delta):
        # находит звезду на плоскости, координаты которой отличаются
        # от i-ой не больше, чем на delta пикселей
        good = (i for i in self._objects if (abs(i.cx - screenX) + abs(i.cy - screenY)) < (delta + i.diameter))
        return min(good, key=lambda i: abs(i.cx - screenX) + abs(i.cy - screenY) - i.diameter, default=None)

    def find_constellation(self, name):
        # находит первую звезду из созвездия с заданным названием name
        # в списке _constellations
        if name in self._constellations:
            return self._constellations[name][0]

    def _get_size(self, mag):
        mag = e ** (self.settings.exp_const + mag * self.settings.exp_factor)
        mag = max(1, mag / self.watcher.radius)
        mag = 0.005 if not self.settings.magnitude else mag / 500
        mag *= self.settings.pull
        return mag

    def _apply_time_rotation(self, star: Star):
        return self.watcher.to_horizontal(star.position), star

    # функция отрисовки звезды. Возвращает данные для отрисовки в функцию draw_object из renderer
    def project_star(self, pos: Horizontal, star: Star):
        # находим диаметр звезды
        diameter = self._get_size(star.magnitude if star is not None else -1)
        # если угол между направлением взгляда камеры и направлением на звезду <=
        # радиусу обзора, то звезда отображается на экране
        if self.watcher.see.angle_to(pos) <= self.watcher.radius:
            # вычисляем изменение координаты звезды относительно направления камеры и проецируем на плоскость экрана
            delta = pos.to_point() - self.watcher.see.to_point()
            prj_delta = delta.rmul_to_matrix(self.watcher.transformation_matrix)
            # используем функцию distortion которая на основе координат в трехмерном пространстве и радиуса обзора
            #         # камеры вычисляет искажение изображения, а именно смещение координат и уменьшение диаметра звезды
            dx, dy = self._distortion(prj_delta.x, prj_delta.y, self.watcher.radius, prj_delta.z)
            diameter, _ = self._distortion(diameter, 0, self.watcher.radius, prj_delta.z)
            # вычисляются координаты отрисовки эллипса на плоскости экрана
            cx, cy = self.centre[0] + dx, self.centre[1] + dy
            return ProjectedStar(cx, cy, diameter, star)
