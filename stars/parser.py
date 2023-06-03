import re
import os

from geometry.equatorial import SecondEquatorial
from stars.star import Star


# TODO: change regexpes!!!
# TODO: rename static methods!!!
# TODO: make refactoring

# в каждом файле директории stars лежит информация про звезды соответствующего созвездия.
# parser парсит из этого файла характеристики звезды, такие как: Right ascension, declination,
# stellar classification, масса и тд

class TxtDataBaseParser:
    def __init__(self):
        regex_str_beginning = r" *?\w+ *?"  # шаблон для поиска всей строки с данными о звезде
        regex_str_alpha = r"(?P<a_hours>\d+): ?(?P<a_minutes>\d+): ?(?P<a_seconds>\d+\.\d+)"  # шаблон для поиска Alf: [0; 23] : [0; 59] : [0; 59] - time : hours : minutes : seconds
        regex_str_alpha_to_delta = r" "  # промежуток между альфа и дельта
        regex_str_delta = r"(?P<d_degrees>[\+-] ?\d+): ?(?P<d_minutes>\d+): ?(?P<d_seconds>\d+)"  # шаблон для поиска Delta: [-90; 90] : [0; 59] : [0; 59] - degree : degree minutes : degree seconds
        regex_str_delta_to_m = r" *?\d+\.\d+ *?-? ?\d+\.\d+.*?"  # от дельта до массы
        regex_str_m = r"(?P<m>\d+\.\d+)"  # шаблон для поиска массы
        regex_str_class = r".*?(?P<class>[OBAFGKM])"  # класс звезды

        regex_str = regex_str_beginning + regex_str_alpha + regex_str_alpha_to_delta + regex_str_delta + regex_str_delta_to_m + regex_str_m + regex_str_class
        self._regex = re.compile(
            regex_str)  # собираем в один шаблон, тем самым вытаскивая из каждой строчки только нужные данные
        # итого, self._regex это полный шаблон

    def parse_dir(self, dirname: str):  # парсит директорию stars
        stars = []
        for filename in os.listdir(dirname):
            # os.listdir return a list containing the names of the files in the directory.
            if filename.endswith('.txt'):  # обрабатываем только тхт файлы
                stars += self.parse_file(os.path.join(dirname, filename),
                                         filename.split('.')[0])  # парсим все звезды в каждом файле
                #конкретнее:
                #первый аргумент - берет название файла
                #второй аргумент(filename.split('.')[0]) берет из названия файла только название созвездия
        return stars  # возвращаем набор звезд

    def parse_file(self, filename: str, constellation: str) -> list:
        # по названию созвездия возвращает stars
        with open(filename, 'r') as file:
            stars = []
            for line in file.readlines():
                star = self.parse_star(line, constellation) #парсит каждую линию
                if star is not None:
                    stars.append(star)
            return stars

    def parse_star(self, line: str, constellation: str) -> Star:  # парсит звезду
        # на вход дается линия в базе данных и название созвездия
        match = self._regex.match(line)  # match - общий шаблон для этой линии в файле
        if match is None:
            return None
        alpha = self._parse_alpha(match)  # парсим альфа. в alpha лежит float
        delta = self._parse_delta(match)  # парсим дельта. в delta лежит float
        m = self._parse_m(match)  # парсим массу
        spectral_class = self._parse_class(match)
        return Star(SecondEquatorial(alpha, delta), m, constellation, spectral_class)

    @staticmethod
    def _parse_delta(match):  # парсит дельта
        # match ищет соответствие шаблону в начале строки
        # match.group - то же самое, только может принимать много аргументов
        # если аргумент один - возвращает одну строчку, если несколько, tuple из строк соответствующих шаблону
        degrees = match.group('d_degrees')
        degrees = degrees.replace(' ', '')
        minutes = match.group('d_minutes')
        seconds = match.group('d_seconds')
        return float(degrees) + float(minutes) / 60 + float(seconds) / 3600  # переводим все из строк

    @staticmethod
    def _parse_alpha(match):  # парсит альфа. на вход принимается общий шаблон
        hours = match.group('a_hours')
        minutes = match.group('a_minutes')
        seconds = match.group('a_seconds')
        return (float(hours) + float(minutes) / 60 + float(seconds) / 3600) * 15

    @staticmethod
    def _parse_m(match):  # на вход принимается общий шаблон match
        m = match.group('m')  # ищем по конкретному шаблону m( для поиска массы)
        return float(m)

    @staticmethod
    def _parse_class(match):
        spectral_class = match.group('class')
        return spectral_class
