from graphics.autogui.gui import GUI
from graphics.autogui.set_item import CheckBoxSet
from graphics.sky_viewers.items.range_item import RangeItem
from stars.filter import Filter


class FilterItem(GUI):
    def __init__(self, selector: Filter, constellations, handler):
        super().__init__("FILTER")
        self.magnitude = self.add(RangeItem(selector, "magnitude", -1, 10))
        self.constellations = self.add(CheckBoxSet(sorted(constellations), selector.constellations, handler))
