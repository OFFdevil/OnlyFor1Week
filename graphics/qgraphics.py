import datetime

from PyQt5 import QtWidgets

from graphics.renderer.camera import Camera
from graphics.crenderer import ControllableRenderer
from stars.skybase import SkyBase


# создаем класс, которой наследуется от QtWidgets.QMainWindow
class StarsWindow(QtWidgets.QMainWindow):
    """Главное окно приложения"""

    def __init__(self, observer: Camera, sky_sphere: SkyBase, start_time: datetime.datetime):
        # создаем конструктор
        # наследуем от классов camera, skysphere
        super().__init__()

        self.resize(700, 700)  # задаем размеры окна
        # используем методы созданные ранее в ControllableRenderer
        self._sky_watch = ControllableRenderer(observer, sky_sphere, start_time)
        self._init_ui()
        self._sky_watch.setFocus()  # устанавливаем фокус на само окно

    def _init_ui(self):
        # создаем виджет panel и устанавливаем его как центральный виджет (наследник от QMainWidget)
        panel = QtWidgets.QWidget()
        self.setCentralWidget(panel)

        # создаем элемент layout c использованием сеточного размещения QGridLayout
        layout = QtWidgets.QGridLayout()
        # устанавливаем его в виджет panel
        panel.setLayout(layout)
        # добавляем новый виджет в ячейку (0, 0) в layout
        layout.addWidget(self._sky_watch, 0, 0)

        self.setWindowTitle("Sky")  # назвали так окно
        self.show()
