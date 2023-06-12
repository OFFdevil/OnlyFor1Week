import datetime
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from graphics.autogui.cast_tools import to_widget
from graphics.sky_viewers.image_viewer import ImageViewer
from utility import profile
from stars.filter import Filter
from graphics.renderer.renderer import Renderer
from graphics.sky_viewers.settings import ControllableSkySettings
from graphics.renderer.watcher import Watcher
from stars.skydatabase import SkyDataBase


class Sky(QMainWindow):  # окно со звездным небом
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase,
                 filter: Filter):  # атрибуты - наблюдатель, база данных звезд и фильтр
        super().__init__()

        self.renderer = Renderer(watcher)  # наблюдатель
        self.settings = ControllableSkySettings()

        self._available_constellations = sky_base.constellations  # выбранные пользователем созвездия
        self._objects = []
        self._sky_sphere = sky_base
        self.filter = filter  # текущий фильтр для звезд

        # QTimer - работа с таймером

        self._create_ui()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.rerender)
        self.timer.setInterval(33)
        self.timer.start()

        self.renderer.settings.pull = 0
        self._i = 0
        self._switcher = 0
        self._rdelay = 1
        self.forecast_step = 10

        self.rerender()

    def _create_ui(self):  # создаем интерфейс звездного неба
        main = QtWidgets.QGridLayout()  # создаем сеточный макет main
        main.setContentsMargins(0, 0, 0,
                                0)  # (int left, int top, int right, int bottom) - устанавливаем поля для использования вокруг макета
        main.setSpacing(0)  # устанавливаем интервалы 0 по вертикали и горизонтали
        self.viewer = ImageViewer()  # создаем
        main.addWidget(self.viewer, 0, 0)
        self._filter_widget = QWidget()
        main.addWidget(self._filter_widget, 0, 1)
        self._filter_widget.setVisible(False)

        self._configurator_widget = QWidget()
        main.addWidget(self._configurator_widget, 0, 2)

        main.setColumnStretch(0, 0)
        main.setColumnStretch(0, 2)

        self._main = main

        self.setWindowTitle("Space Simulator")
        self.resize(1000, 700)
        self.setCentralWidget(to_widget(main))
        self.show()
        self.setFocus()
        self.setMouseTracking(True)
        self.setVisible(True)

    def _update_image(self):
        # self.viewer.width() и height - текущая ширина и высота объекта, устанавливаем их
        self.renderer.width = self.viewer.width()
        self.renderer.height = self.viewer.height()
        # генерируем новое изображение на основе объекта objects
        image = self.renderer.render(self._sky_sphere.get_stars(self.filter), self._switcher > 1)
        if self.forecast_step > 0:
            self._switcher = (self._switcher + 1) % self.forecast_step
        # устанавливаем новое изображение
        self.viewer.image = image

    @profile
    def rerender(self, exec_delta: datetime.timedelta):
        if exec_delta is None:
            return
        self._rdelay = exec_delta.microseconds / 1000
        self.renderer.watcher.local_time += exec_delta * self.settings.second_per_second
        # обновление локального времени в переменной
        self._update_image()  # обновляем изображение
        if self._i <= 25:
            self.renderer.settings.pull = self._i / 25
            self._i += 1
        else:
            self.renderer.settings.pull = 1
        self._update_image()

    def mousePressEvent(self, QMouseEvent):
        self.setFocus()

    @property
    def delay(self):
        return self.timer.interval()

    @delay.setter
    def delay(self, value):
        self.timer.setInterval(value)
