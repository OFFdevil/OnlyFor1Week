import datetime
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from graphics.autogui.cast_tools import to_widget
from graphics.sky_viewers.image_viewer import ImageViewer
from graphics.sky_viewers.utility import profile
from graphics.renderer.renderer import Renderer
from graphics.renderer.settings import ControllableRenderSettings
from graphics.renderer.watcher import Watcher
from stars.skydatabase import SkyDataBase


class Sky(QMainWindow):  # окно со звездным небом
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase):  # атрибуты - наблюдатель и база данных звезд
        super().__init__()

        self._renderer = Renderer(watcher)  # наблюдатель
        self.settings = ControllableRenderSettings()

        self._available_constellations = sky_base.constellations  # выбранные пользователем созвездия
        self._objects = []
        self._sky_sphere = sky_base

        # QTimer - работа с таймером

        self._create_ui()
        self.setFocus()  # передает фокус ввода с клавиатуры этому виджету, если этот виджет или один из его родителей является активным окном.

        self._timer = QtCore.QTimer(self)  # создаем таймер
        self._timer.timeout.connect(self._rerender)  # соединяем таймер с тем, что будем обрабатывать
        self._timer.setInterval(33)  # устанавливаем интервал 33 милисекунды

        self._rerender()
        self._timer.start()  # запуск таймера

        self.setVisible(True)

    def _create_ui(self):  # создаем интерфейс звездного неба
        main = QtWidgets.QGridLayout()  # создаем сеточный макет main
        main.setContentsMargins(0, 0, 0,
                                0)  # (int left, int top, int right, int bottom) - устанавливаем поля для использования вокруг макета
        main.setSpacing(0)  # устанавливаем интервалы 0 по вертикали и горизонтали
        self.viewer = ImageViewer()  # создаем
        main.addWidget(self.viewer, 0, 0)
        main.setColumnStretch(0, 1)

        self._main = main

        self.setWindowTitle("Space Simulator")
        self.resize(1000, 700)
        self.setCentralWidget(to_widget(main))
        self.show()
        # создаем конфигуратор, который позволяет редактировать настройки изображения
        # он размещается во втором столбце главного макета, таким образом, пользователь может редактировать
        # настройки и в то же время видеть изменения сразу на изображении
        self._configurator_widget = QWidget()
        main.addWidget(self._configurator_widget, 0, 1)

    def _update_image(self):
        # self.viewer.width() и height - текущая ширина и высота объекта, устанавливаем их
        self._renderer.width = self.viewer.width()
        self._renderer.height = self.viewer.height()
        # генерируем новое изображение на основе объекта objects
        image = self._renderer.render(self._objects)
        # устанавливаем новое изображение
        self.viewer.image = image

    @profile
    def _rerender(self, exec_delta: datetime.timedelta):
        if exec_delta is None:
            return

        self._renderer.watcher.local_time += exec_delta * self.settings.second_per_second
        self._update_image()

    def mousePressEvent(self, QMouseEvent):
        self.setFocus()

    @property
    def delay(self):
        return self._timer.interval()

    @delay.setter
    def delay(self, value):
        self._timer.setInterval(value)
