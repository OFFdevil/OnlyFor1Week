import math

import numpy

from geometry.equatorial import SecondEquatorial
from geometry.point import Point


def rescale_angle_distance(sight_radius, visible_radius, dist):  # пересчет расстояния от точки наблюдения
    # с радиусом видимости sight_radius до расстояния visible_radius - определяет радиус
    # видимости объектов
    return dist / sight_radius * visible_radius  # масштабирует расстояние


def translate_coordinates(sight_radius, visible_radius, r, sight_vector, diametr, ox, oy, point: SecondEquatorial):
    # преобразует координаты объектов в небесной сфере относительно точки наблюдения
    # в координаты на экране
    r = rescale_angle_distance(sight_radius, visible_radius, r)  # r - расст от наблюдателя до объекта

    cos_da = sight_vector.get_relative_angle_cos(point)  # косинус азимута
    sin_da = sight_vector.get_relative_angle_sin(point)  # синус азимута
    cx, cy = ox - r * sin_da, oy - r * cos_da  # перевод расположения объекта в небесной сфере
    # в координаты на плоскости экрана
    # считаем координаты центра объекта

    x, y = cx - diametr // 2, cy - diametr // 2  # координаты левого верхнего угла
    return x, y  # возвращает координаты объекта


def get_angle(x1, y1, x2, y2):  # вычисляет угол между двумя векторами, которые заданы
    # координатами концов векторов
    return math.atan2(x1 * x2 + y1 * y2, x1 * y2 - x2 * y1)


def get_see_distance(width, height, angle):  # вычисляет дистанцию видимости на основе
    # угла обзора и размера экрана
    angle = math.radians(angle) / 2  # перевод угла в радианы
    radius = min(width, height) / 2  # радиус экрана
    return radius / math.tan(angle)  # расстояние дальней точки видимости от наблюдателя


def project(point: SecondEquatorial, see: SecondEquatorial, see_distance: float):
    # проецирует две точки на экран - точка в небесной сфере и точка обзора (see)
    da = point.alpha - see.alpha
    dd = point.delta - see.delta
    dx = math.tan(da) * see_distance
    dy = math.tan(dd) * see_distance
    return dx, dy  # возвращает координаты проекции в виде кортежа


def solve(a00, a01, a10, a11, b0, b1):  # функция решает систему уравнений методом Гаусса
    a = numpy.array([[a00, a01], [a10, a11]])
    b = numpy.array([b0, b1])
    try:
        return numpy.linalg.solve(a, b)
    except:
        return None  # если решений у системы нет


def extract_2d(point: Point, see: Point, up: Point):  # преобразует координаты в 3д
    # в набор координат на плоскости
    # используем координаты точек point, see, up, чтобы определить переменные слу
    a = solve(see.x, up.x, see.y, up.y, point.x, point.y)
    b = solve(see.x, up.x, see.z, up.z, point.x, point.z)
    c = solve(see.y, up.y, see.z, up.z, point.y, point.z)
    return a if not a is None else (b if not b is None else c)  # координаты точки на экране
