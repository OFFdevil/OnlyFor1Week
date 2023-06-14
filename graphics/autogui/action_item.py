from PyQt5.QtWidgets import QPushButton

from graphics.autogui.gui import GUI


class ActionItem(GUI):
    def __init__(self, name: str, action):
        super().__init__("")
        self._name = name
        self._action = action
        self._widget = QPushButton(name)
        self.layout.addWidget(self._widget)
        self._widget.clicked.connect(action)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def try_save(self):
        pass

    def try_load(self):
        pass
