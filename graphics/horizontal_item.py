import re

from geometry.horizontal import Horizontal
from graphics.autogui.field_item import FieldItem


# класс, отвечающий за item в горизонтальной системе координат
class HorizontalItem(FieldItem):
    # TODO: move to Horizontal
    @staticmethod
    def parse_str(s, regexp):  # парсит строку(a и d вектора в горизонт коорд) по данной регулярке
        match = regexp.match(s)
        if match is None:
            print("!")
            raise ValueError()
        groups = match.groupdict()
        if (not ("a" in groups)) or (not ("d" in groups)):
            print("!!")
            raise ValueError()
        print(groups["a"], groups["d"])
        return Horizontal(float(groups["a"]), float(groups["d"]))

    def __init__(self, obj: object, fname: str, ro: bool = False):
        pregex = "^\(?(?P<a>[+-]?[\d.]+?), ?(?P<d>[+-]?[\d.]+?)\)?$"  # сама регулярка
        cpregexp = re.compile(pregex)
        builder = str
        parser = lambda s: HorizontalItem.parse_str(s, cpregexp)  # парсер. принимает строку s возвращает
        # объект типа horizontal
        super().__init__(obj, fname, builder, parser, ro)  # инициализируем HorizontalItem
