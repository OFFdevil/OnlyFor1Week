from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget


def to_widget(layout: QGridLayout, bcolor: str = None):
    widget = QWidget()
    widget.setMouseTracking(True)
    widget.setLayout(layout)
    if bcolor is not None:
        widget.setStyleSheet("QWidget {{ border: 1px solid {} }}".format(bcolor))
    return widget
