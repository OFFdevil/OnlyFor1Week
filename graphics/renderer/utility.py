from PyQt5.QtGui import QColor


# принимает строку в формате шестнадцатеричного кода цвета и преобразует ее в объект `QColor`
def hexstr_to_color(s: str):
    # разбиение входной строки на три части и преобразование в десятичные числа
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:], 16)
    return QColor(r, g, b)


def try_or_print(foo):
    def decorated(*args, **kwargs):
        try:
            return foo(*args, **kwargs)
        except Exception as e:
            print(e)
            return None

    return decorated
