from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit

from graphics.autogui.item import Item


def camel_case_to_normal(s: str):
    return s.replace('_', ' ')


class TextItem(Item):
    def __init__(self, name: str, setter, getter, ro: bool, label: str = None):
        super().__init__()
        self._setter = setter
        self._getter = getter
        self._name = name
        self._widget = QLineEdit()
        self._edit_mode = False
        self._apply_edit = False
        label = label if label is not None else camel_case_to_normal(name)
        self.layout.addWidget(QLabel(label), 0, 0)
        self.layout.addWidget(self._widget, 0, 1)
        self._widget.returnPressed.connect(self._inverse_editing)
        self._widget.setReadOnly(ro)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def _inverse_editing(self):
        self._edit_mode = not self._edit_mode
        if self._edit_mode:
            self._widget.setStyleSheet("QLineEdit { background: rgb(192, 192, 192);}")
        else:
            self._apply_edit = True
            self._widget.setStyleSheet("QLineEdit { background: rgb(255, 255, 255);}")

    def try_save(self):
        if not self._edit_mode and self._apply_edit:
            self._apply_edit = False
            try:
                self._setter(self._widget.text())
                return False
            except:
                pass
        self._apply_edit = False
        return False

    def try_load(self):
        if not self._edit_mode:
            s = self._getter()
            self._widget.setText(s)
