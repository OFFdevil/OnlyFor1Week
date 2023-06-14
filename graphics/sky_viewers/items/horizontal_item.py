import re

from geometry.horizontal import Horizontal
from graphics.autogui.field_item import FieldItem


class HorizontalItem(FieldItem):
    @staticmethod
    def parse_str(s, regexp):
        match = regexp.match(s)
        if match is None:
            raise ValueError()
        groups = match.groupdict()
        if (not ("a" in groups)) or (not ("d" in groups)):
            raise ValueError()
        return Horizontal(float(groups["a"]), float(groups["d"]))

    def __init__(self, obj: object, fname: str, ro: bool = False, label=None):
        pregex = "^\(?(?P<a>[+-]?[\d.]+?), (?P<d>[+-]?[\d.]+?)\)?$"
        cpregexp = re.compile(pregex)
        builder = str
        parser = lambda s: HorizontalItem.parse_str(s, cpregexp)
        super().__init__(obj, fname, builder, parser, ro, label)
