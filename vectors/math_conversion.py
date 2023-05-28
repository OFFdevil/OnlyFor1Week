from math import pi


def to_degree(radian):  # перевод из радиан в градусы
    return 180.0*radian/pi


def to_radian(degree):  # перевод из градусов в радианы
    return pi*degree/180
