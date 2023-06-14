from PyQt5.QtWidgets import QLabel
from graphics.autogui.item import Item


class LabelItem(Item):
    def __init__(self, label: str, bold: bool = False):
        super().__init__()
        fstr = "<b>{}</b>" if bold else "{}"
        src = QLabel(fstr.format(label))
        self.addWidget(src)
