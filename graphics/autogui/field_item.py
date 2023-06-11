import datetime

from graphics.autogui.text_item import TextItem


# создаем классы для создания элементов пользовательского интерфейса
def get_attribute(obj, fname):
    current = obj
    for part in fname.split('.'):
        current = current.__getattribute__(
            part)  # __getattribute__ Вызывается при попытке доступа к атрибуту сurrent типа object
    return current


def set_attribute(obj, fname, value):  # используется для установки значения
    # заданного атрибута объекта, используя строку с именем атрибута
    current = obj
    for part in fname.split('.')[:-1]:
        current = current.__getattribute__(part)
    current.__setattr__(fname.split('.')[-1], value)


class FieldItem(TextItem):  # определяет общие методы и свойства для элементов пользовательского интерфейса
    def __init__(self, obj: object, fname: str, builder, parser, ro: bool, label=None):
        setter = lambda v: set_attribute(obj, fname, parser(v))
        getter = lambda: builder(get_attribute(obj, fname))
        super().__init__(fname, setter, getter, ro, label)


class IntItem(FieldItem):  # представляет элементы пользовательского интерфейса для целочисленных значений
    def __init__(self, obj: object, fname: str, ro: bool = False):
        super().__init__(obj, fname, str, int, ro)


class FloatItem(FieldItem):  # представляет элементы пользовательского интерфейса для дробных значений
    def __init__(self, obj: object, fname: str, ro: bool = False):
        builder = lambda f: str(f) if int(f) != f else str(int(f))
        super().__init__(obj, fname, builder, float, ro)


class StringItem(FieldItem):  # представляет элементы пользовательского интерфейса для строковых значений
    def __init__(self, obj: object, fname: str, ro: bool = False):
        super().__init__(obj, fname, lambda a: a, lambda a: a, ro)


class DateTimeItem(FieldItem):  # элемент пользовательского интерфейса для даты и времени
    # он использует преобразователи, чтобы преобразовать значения Python-даты и времени в строки и обратно
    def __init__(self, obj: object, fname: str, ro: bool = False):
        self.format = "%d.%m.%Y %H:%M:%S"
        parser = lambda s: datetime.datetime.strptime(s, self.format)
        builder = lambda d: d.strftime(self.format)
        super().__init__(obj, fname, builder, parser, ro)
# Эти классы позволяют связать атрибуты объектов Python со значениями элементов пользовательского интерфейса
# и обрабатывать изменения значений пользовательского интерфейса,
# чтобы изменять соответствующие атрибуты объектов Python и наоборот
