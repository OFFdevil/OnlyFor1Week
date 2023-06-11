from PyQt5.QtWidgets import QCheckBox

from graphics.autogui.field_item import set_attribute, get_attribute
from graphics.autogui.item import Item


class BoolItem(Item):  # класс отвечающий за selectable buttons(за квадратики где либо стоит галочка либо нет)
    def __init__(self, obj: object, fname: str):
        super().__init__()
        self._widget = QCheckBox(fname)  # создаем виджет
        self.layout.addWidget(self._widget)
        self._buffer = None
        self._lock = False
        self._setter = lambda v: set_attribute(obj, fname,
                                               v)  # сеттер/геттер устанавливаем как соотв. функции из FieldItem
        self._getter = lambda: get_attribute(obj, fname)
        self._widget.stateChanged.connect(self._on_changed)

    def _on_changed(self):  # функция которая вызывается при изменении состояния boolItem
        if self._lock:
            return
        s = self._widget.checkState() != 0
        self._buffer = s

    def try_save(self):
        if self._buffer != None:
            try:
                self._setter(self._buffer)
                self._buffer = None
                return False
            except:
                self._buffer = None
        return False

    def try_load(self):
        if self._buffer == None:
            v = self._getter()
            self._lock = True
            self._widget.setChecked(2 if v else 0)
            self._lock = False
