from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget


# cast_tools отвечает за создание виджета по переданному макету и цвету

def to_widget(layout: QGridLayout, bcolor: str = None):
    widget = QWidget()  # создаем виджет
    widget.setMouseTracking(True)
    # включаем отслеживание мыши(т е виджет получает события перемещения
    # мыши даже если кнопки не нажимаются)
    widget.setLayout(layout)  # устанавливаем ему макет layout
    if bcolor is not None:
        widget.setStyleSheet("QWidget {{ border: 1px solid {} }}".format(bcolor))  # setStyleSheet устанавливает цвет
    return widget
