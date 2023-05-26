from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from graphics.renderable import Renderable


class Renderer(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.show()
        self._objects = []
        self.bckg_color = QColor(0, 0, 0)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(self.bckg_color))
        painter.end()

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, value):
        self._objects = []
        for i in value:
            if not isinstance(i, Renderable):
                raise TypeError("Can not render '" + str(i) + "'")
            self._objects.append(i)
        self.repaint()