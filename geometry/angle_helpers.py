from stars.sky_math import sign


def to_0_360(degree):  # делаем так, чтобы значение угла лежало в промежутке между 0 и 360
    md = sign(degree) * (abs(degree) % 360)
    return (md + 360) % 360


def to_cos_period_cutted(degree):  # принимаем на вход угол, приводим его значение к интервалу
    # от -90 до 90
    if -90 <= degree <= 90:
        return degree
    if degree < -90:
        return -90
    return 90


def time_to_seconds(h, m, s):  # конвертация времени в секунда
    return float(h) * 3600 + float(m) * 60 + float(s)


def seconds_to_degree(s):  # конвертация секунд в звездные градусы, 1 звездный час = 15 зв градусов
    return s * 15 / 3600


def time_to_degree(h, m, s):  # конвертация времени в звездные градусы
    return seconds_to_degree(time_to_seconds(h, m, s))


def dtime_to_degree(degree, dm, ds):  # принимает градусы, минуты и секунды для долготы и широты,
    # потом приводит их к звездным градусам
    return sign(degree) * (abs(degree) + dm / 60 + ds / 3600)


def apply(operation, *degrees):  # применяет указанную операцию к списку переданных аргументов
    # применяем функции преобразований градусов к списку переданных аргументов
    res = []
    for i in degrees:
        res.append(operation(i))
    return res  # возвращает список результатов
