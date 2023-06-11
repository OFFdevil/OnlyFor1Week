import re
from graphics.autogui.field_item import FieldItem
from graphics.autogui.gui import GUI
from graphics.autogui.slide_item import SlideItem
from stars.filter import Range


# класс, отвечающий за два ползунка в меню: по минимуму и по максимуму размера звезды

class RangeItem(GUI):
    def __init__(self, obj: object, fname: str, min, max, label=None):
        super().__init__(fname)
        self.min = self.add(SlideItem(obj, fname + ".auto_min", min, max, "min"))
        self.min = self.add(SlideItem(obj, fname + ".auto_max", min, max, "max"))