import re
import os

from geometry.avector import Equatorial
from stars.sky_math import TimeHelper
from stars.skybase import SkyBase
from stars.star import Star


# TODO: change regexpes!!!
# TODO: rename static methods!!!
# TODO: make refactoring

# в каждом файле директории stars лежит информация про звезды соответствующего созвездия.
# parser парсит из этого файла характеристики звезды, такие как: Right ascension, declination,
# stellar classification, масса и тд

# Alf: [0; 23] : [0; 59] : [0; 59] - time : hours : minutes : seconds
# Del: [-90; 90] : [0; 59] : [0; 59] - degree : degree minutes : degree seconds

# вспомогательные функции

def num_regexp(name: str):  # функция общего вида регулярного выражения для числа (по названию)
    return r"(?P<{}>[\+-]? *?[\d\.]+)".format(name)


def any_num_regexp(separator: str, name: str, count: int):  # функция общего вида регулярного выражения для неск. чисел
    tmp = ""
    for i in range(0, count - 1):
        tmp += num_regexp(name + '_' + str(i)) + "{} ?".format(separator)
    tmp += num_regexp(name + '_' + str(count - 1))
    return tmp


print(
    any_num_regexp(':', "alf", 3))  # пример, парсим Alf: [0; 23] : [0; 59] : [0; 59] - time : hours : minutes : seconds


def extract_nums(parsed, name: str, count: int):  # функция извлечения распарсенных чисел
    nums = []
    for i in range(0, count):
        nm = name + '_' + str(i)
        if nm in parsed:
            nums.append(float(parsed[nm].replace(' ', '')))
        else:
            raise ValueError()
    return nums


class TxtDataBaseParser:  # сам парсер
    def __init__(self):
        map_re = r"^ *?{} *?".format(num_regexp("map"))  # создаем регулярку по шаблону для считывания номера map
        pos_re = any_num_regexp(':', 'alf', 3) + ' ' + any_num_regexp(':', 'del', 3)  # регулярки для альфа, дельта
        self._regex = re.compile(map_re + pos_re)  # из двух шаблонов регулярных выражений один объект

    def parse(self, line_const_tuples):
        stars = [i for i in (self.parse_star(t) for t in line_const_tuples) if i is not None]  # генератор
        return SkyBase(stars)  # заполняем базу данных звезд

    def parse_star(self, pair) -> Star:  # парсим звезду
        try:
            parsed = self._regex.match(pair[0]).groupdict()
            a_h, a_m, a_s = extract_nums(parsed, 'alf', 3)
            d_d, d_m, d_s = extract_nums(parsed, 'del', 3)
            a = TimeHelper.time_to_degree(a_h, a_m, a_s)
            d = TimeHelper.time_to_degree(0, d_m, d_s) + d_d
            return Star(Equatorial(a, d), pair[1])
        except Exception as ex:
            print(ex)
