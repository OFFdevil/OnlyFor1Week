from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit

from graphics.autogui.item import Item
from graphics.autogui.label import Label


class TextItem(Item):
    def __init__(self, name: str, setter, getter, ro: bool):  # настраивает виджет
        super().__init__()
        self._setter = setter
        self._getter = getter
        self._name = name
        self._widget = QLineEdit()
        self._edit_mode = False  # false <=> не происходит редактирования
        self._apply_edit = False  # false <=> настройки не применены
        self.addWidget(QLabel(name), 0, 0)  # виджет для названия параметра
        self.addWidget(self._widget, 0, 1)  # виджет для изменения значения параметра
        self.setSpacing(1)  # все внутренние расстояния между виджетами = 1
        self._widget.returnPressed.connect(self._inverse_editing)  # вызывает метод при нажатии
        # клавиши энтер
        self._widget.setReadOnly(ro)

    def _inverse_editing(self):  # находится ли виджет в режиме
        # редактирования
        self._edit_mode = not self._edit_mode
        if self._edit_mode:
            self._widget.setStyleSheet("QLineEdit { background: rgb(192, 192, 192);}")
            # если да то серый фон
        else:
            self._apply_edit = True
            self._widget.setStyleSheet("QLineEdit { background: rgb(255, 255, 255);}")
            # если нет то белый фон

    def try_save(self):  # пытается сохранить изменения значения параметра
        if not self._edit_mode and self._apply_edit:
            self._apply_edit = False
            try:
                self._setter(self._widget.text())
                return False
            except Exception as ex:
                print(str(ex))
        self._apply_edit = False
        return False

    def try_load(self):  # загружает текущее значение параметра объекта
        # в поле ввода, если виджет не в режиме редактирования
        if not self._edit_mode:
            s = self._getter()
            self._widget.setText(s)
