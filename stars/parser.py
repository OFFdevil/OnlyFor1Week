import re

from geometry.angle_helpers import dtime_to_degree, time_to_degree
from geometry.equatorial import Equatorial
from stars.skydatabase import SkyDataBase
from stars.star import Star, SPECTRAL_CLASSES


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
        tmp += num_regexp(name + '_' + str(i)) + "{} *?".format(separator)
    tmp += num_regexp(name + '_' + str(count - 1))
    return tmp


SPECTRAL_CLASSES_SET = str.join('', SPECTRAL_CLASSES) #далем set

# print(
# any_num_regexp(':', "alf", 3))  # пример, парсим Alf: [0; 23] : [0; 59] : [0; 59] - time : hours : minutes : seconds


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
    def __init__(self):  # создаем шаблон, по которому будем считывать строчку информации про звезду
        map_re = r"^ *?{} *?".format(num_regexp("map"))  # создаем регулярку по шаблону для считывания номера map
        pos_re = any_num_regexp(':', 'alf', 3) + ' ' + any_num_regexp(':', 'del', 3)  # регулярка для альфа, дельта
        sp0_re = " +?" + any_num_regexp(' ', 'trash0', 2) + r' *?\w*? *?'
        mag_re = num_regexp("mag")
        cls_re = ' +?[a-z:]*?' + '(?P<cls>[A-Z]).*? +?'
        sp1_re = any_num_regexp(' ', 'trash1', 2) + '...' + any_num_regexp(' ', 'trash2', 3)
        nam_re = r' +?\d*?(?P<name>[a-zA-Z]*?)? *?\d*? *?(\(.*?\))?$'
        self._regex = re.compile(map_re + pos_re + sp0_re + mag_re + cls_re + sp1_re + nam_re)

    def parse(self, line_const_tuples):
        stars = [s for s in (self.parse_star(t) for t in line_const_tuples) if s is not None]  # генератор
        return SkyDataBase(stars)  # заполняем базу данных звезд

    def parse_star(self, pair) -> Star:  # парсим звезду(коорд, созвездие, магнитуду, спект. класс и имя)
        try:
            parsed = self._regex.match(pair[0].replace('\n', '')).groupdict()
            a_h, a_m, a_s = extract_nums(parsed, 'alf', 3)
            d_d, d_m, d_s = extract_nums(parsed, 'del', 3)
            a = time_to_degree(a_h, a_m, a_s)
            d = dtime_to_degree(d_d, d_m, d_s)
            cls = parsed['cls'] if parsed['cls'] in SPECTRAL_CLASSES else ''
            return Star(Equatorial(a, d), pair[1], float(parsed['mag']), cls, parsed['name'])
        except Exception as ex:
            print('Can`t parse line ({}) in {}'.format(*pair))
