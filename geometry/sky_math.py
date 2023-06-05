from math import cos, sin


class FirstEquatorialToHorizontal:  # перевод из первой экваториальной в горизонтальную
    '''https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D1%82%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D0%BA%D0%BE%D0%BE%D1%80%D0%B4%D0%B8%D0%BD%D0%B0%D1%82'''

    # далее функции для перехода из первой экваториальной
    # f-широта
    # t- часовой угол светила
    # d-склонение светила
    # z-Зенитное расстояние z
    # a-Азимут светила
    @staticmethod
    def cosz(f, d, t):
        return sin(f) * sin(d) + cos(d) * cos(f) * cos(t)

    @staticmethod
    def siza_sinz(d, t):
        return cos(d) * sin(t)

    @staticmethod
    def cosa_sinz(f, d, t):
        return -cos(f) * sin(d) + sin(f) * cos(d) * cos(t)
