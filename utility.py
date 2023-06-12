import datetime
from PyQt5.QtGui import QColor


def profile(foo):  # декоратор функции profile
    # записывает информацию о времени выполнения и времени, прошедшего с последнего вызова
    def decorated(*args, **kwargs):
        prev = foo.__last_call_time if "__last_call_time" in dir(foo) else None
        lct = foo.__last_call_time = datetime.datetime.now()
        kwargs["exec_delta"] = (lct - prev) if not prev is None else None
        return foo(*args, **kwargs)
    return decorated


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
            print("Exception in {}({}; {}): {}".format(foo.__name__, e, args, kwargs))
            return None

    return decorated
