import re
from graphics.autogui.field_item import FieldItem
from graphics.autogui.gui import GUI
from graphics.autogui.slide_item import SlideItem
from stars.filter import Range


# класс, отвечающий за два ползунка в меню: по минимуму и по максимуму размера звезды

class RangeItem(GUI):
    def __init__(self, obj: object, fname: str, min, max, label=None):
        super().__init__(fname)
        self.min = self.add(SlideItem(obj, fname + "._minimum", min, max, "min"))
        self.max = self.add(SlideItem(obj, fname + "._maximum", min, max, "max"))
