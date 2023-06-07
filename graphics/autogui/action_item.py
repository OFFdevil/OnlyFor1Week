from PyQt5.QtWidgets import QPushButton

from graphics.autogui.item import Item


# класс, отвечающий за кнопки при нажатии которых происходит действие
class ActionItem(Item):
    def __init__(self, name: str, action):  # создаем кнопку по названию и функции
        super().__init__()
        self._name = name
        self._action = action
        self._widget = QPushButton(name)  # делаем виджет-командную кнопку
        self.addWidget(self._widget)
        self._widget.clicked.connect(action)  # clicked - это signal, который испускается когда кнопка активирвована

    def try_save(self):
        pass

    def try_load(self):
        pass
