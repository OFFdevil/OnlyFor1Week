from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSlider
from graphics.autogui.field_item import set_attribute, get_attribute
from graphics.autogui.item import Item
from graphics.autogui.text_item import camel_case_to_normal


# класс ползунок(для настроек, какие звезды показывать в зависимости от размера)
class SlideItem(Item):
    def __init__(self, obj, name: str, min: int, max: int, label: str = None):
        super().__init__()
        self._setter = lambda v: set_attribute(obj, name, v)
        self._getter = lambda: get_attribute(obj, name)
        self._name = name
        self._widget = QSlider(1)
        label = label if label is not None else camel_case_to_normal(name)
        self.layout.addWidget(QLabel(label), 0, 0)
        self.layout.addWidget(self._widget, 0, 1)
        #        self.setSpacing(1)
        self._edit = False
        self._apply = False
        self._widget.setMinimum(min)
        self._widget.setMaximum(max)
        self._widget.sliderPressed.connect(lambda: self._switch_edit(True))
        self._widget.sliderMoved.connect(lambda i: self._switch_apply(True))

    def _switch_edit(self, value):
        self._edit = value

    def _switch_apply(self, value):
        self._apply = value

    def try_save(self):
        if self._apply:
            self._apply = False
            self._edit = False
            try:
                print(self._widget.value())
                self._setter(self._widget.value())
                return False
            except Exception as ex:
                print(str(ex))
        self._apply = False
        self._edit = False
        return False

    def try_load(self):
        if not self._edit:
            s = self._getter()
            self._widget.setValue(s)
