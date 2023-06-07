from PyQt5.QtWidgets import QLabel
from graphics.autogui.item import Item


class Label(Item):  # наследуется от Item
    def __init__(self, label: str, bold: bool = False):
        # создаем виджет с помощью QLabel, параметры: label, дальше какой шрифт
        super().__init__()
        fstr = "<b>{}</b>" if bold else "{}"
        src = QLabel(fstr.format(label))
        self.addWidget(src)
