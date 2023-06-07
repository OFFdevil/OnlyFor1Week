import datetime

from graphics.autogui.text_item import TextItem


def get_attribute(obj, fname):
    current = obj
    for part in fname.split('.'):
        current = current.__getattribute__(part) # __getattribute__ Вызывается при попытке доступа к атрибуту сurrent типа object
    return current


def set_attribute(obj, fname, value):
    current = obj
    for part in fname.split('.')[:-1]:
        current = current.__getattribute__(part)
    current.__setattr__(fname.split('.')[-1], value)


class FieldItem(TextItem):
    def __init__(self, obj: object, fname: str, builder, parser):
        setter = lambda v: set_attribute(obj, fname, parser(v))
        getter = lambda: builder(get_attribute(obj, fname))
        super().__init__(fname, setter, getter)


class IntItem(FieldItem):
    def __init__(self, obj: object, fname: str):
        super().__init__(obj, fname, str, int)


class FloatItem(FieldItem):
    def __init__(self, obj: object, fname: str):
        builder = lambda f: str(f) if int(f) != f else str(int(f))
        super().__init__(obj, fname, builder, float)


class StringItem(FieldItem):
    def __init__(self, obj: object, fname: str):
        super().__init__(obj, fname, lambda a: a, lambda a: a)


class DateTimeItem(FieldItem):
    def __init__(self, obj: object, fname: str):
        self.format = "%d.%m.%Y %H:%M:%S"
        parser = lambda s: datetime.datetime.strptime(s, self.format)
        builder = lambda d: d.strftime(self.format)
        super().__init__(obj, fname, builder, parser)
