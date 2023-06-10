from stars.sky_math import sign


def to_0_360(degree):
    md = sign(degree) * (abs(degree) % 360)
    return (md + 360) % 360


def to_cos_period_cutted(degree):
    if -90 <= degree <= 90:
        return degree
    if degree < -90:
        return -90
    return 90


def time_to_seconds(h, m, s):
    return float(h) * 3600 + float(m) * 60 + float(s)


def seconds_to_degree(s):
    return s * 15 / 3600


def time_to_degree(h, m, s):
    return seconds_to_degree(time_to_seconds(h, m, s))


def dtime_to_degree(degree, dm, ds):
    return sign(degree) * (abs(degree) + dm / 60 + ds / 3600)


def apply(operation, *degrees):
    res = []
    for i in degrees:
        res.append(operation(i))
    return res
