from graphics.autogui.field_item import FieldItem
from graphics.autogui.gui import GUI
from graphics.autogui.set_item import CheckBoxSet
from graphics.autogui.slide_item import SlideItem
from graphics.sky_viewers.items.range_item import RangeItem
from stars.filter import Filter


# класс, отвечающий за выбор звезд при изменении ползунка
class FilterItem(GUI):
    def __init__(self, filter: Filter, constellations, handler):
        super().__init__("FILTER")
        self.magnitude = self.add(RangeItem(filter, "magnitude", -1, 10))
        self.constellations = self.add(CheckBoxSet(sorted(constellations), filter.constellations, handler))
