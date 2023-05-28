from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from graphics.renderable import Renderable


class Renderer(QWidget):
    # создаем конструктор, наследуем от QWidget
    def __init__(self):
        super().__init__()  # доступ к унаследованным методам от QWidget
        # которые переопределены в классе
        self.setGeometry(300, 300, 300, 220)  # задаем размеры окна
        self.setWindowTitle('Icon')  # заголовок
        self.show()
        self._objects = []  # создали массив, с котором дальше будем работать
        self.bckg_color = QColor(0, 0, 0)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(self.bckg_color))
        painter.end()

    @property  # создали геттер для objects
    def objects(self):
        return self._objects

    @objects.setter  # создали сеттер от objects (название должно быть одинаковым)
    def objects(self, value):
        self._objects = []
        for i in value:  # перебор всех значений массива
            if not isinstance(i, Renderable):
                raise TypeError("Can not render '" + str(i) + "'")
            self._objects.append(i)  # добавление элементов, если не выдана ошибка
        self.repaint()
