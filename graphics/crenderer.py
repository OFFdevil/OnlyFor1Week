import datetime

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QMainWindow

from geometry.avector import Horizontal
from graphics.configurator import Configurator
from graphics.image_viewer import ImageViewer
from graphics.renderer.renderer import Renderer
from graphics.renderer.settings import ControllableRenderSettings
from graphics.renderer.watcher import Watcher
from stars.skybase import SkyBase


# создаем класс ControllableRenderer, который наследуется от QtWidgets.QWidget
# содержит методы для инициализации экрана рендеринга с небесной сферой и камерой, управления и перерисовкой
class StarsWindow(QMainWindow):
    def __init__(self, watcher: Watcher, sky_sphere: SkyBase):
        super().__init__()

        # задаем все методы
        self._canvas = Renderer(watcher)
        self._objects = []
        self._sky_sphere = sky_sphere
        self.settings = ControllableRenderSettings()
        self._key_commands = {
            # прописывание команд, которые выполняются при нажатии клавиш
            # движение вверх, вниз, вправо, влево, уменьшение, увеличение содержимого окна
            QtCore.Qt.Key_A: lambda: self._change_sight_vector(1, 0),
            QtCore.Qt.Key_D: lambda: self._change_sight_vector(-1, 0),
            QtCore.Qt.Key_W: lambda: self._change_sight_vector(0, 1),
            QtCore.Qt.Key_S: lambda: self._change_sight_vector(0, -1),

            QtCore.Qt.Key_Q: lambda: self._change_sight_vector(0, 0, 10),
            QtCore.Qt.Key_E: lambda: self._change_sight_vector(0, 0, -10),
        }

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(1000 / self.settings.fps)
        self._timer.timeout.connect(self._on_timer_tick)

        self._constellations = sky_sphere.constellations

        self._cmodel = QStandardItemModel()
        self._create_ui()
        self.setFocus()

        self._last_tick_time = datetime.datetime.now()
        self._on_timer_tick()  # вызывается при истечении времени таймера и обновляет содержимое окна
        self._timer.start()

    # функция постановки на паузу
    def _switch_pause(self):
        if self._timer.isActive():
            self._timer.stop()
        else:
            self._timer.start()

    def _create_ui(self):
        # создаем главное окно с изображением, размером 100*700 и названием Sky
        main = QtWidgets.QGridLayout()
        self.viewer = ImageViewer()
        main.addWidget(self.viewer, 0, 0)
        main.setColumnStretch(0, 1)

        self.setWindowTitle("Sky")
        self.resize(1000, 700)
        panel = QtWidgets.QWidget()
        # создаем панель центрального виджета
        panel.setLayout(main)
        self.setCentralWidget(panel)
        self.show()

        # создаем конфигуратор, который позволяет редактировать настройки изображения
        # он размещается во втором столбце главного макета, таким образом, пользователь может редактировать
        # настройки и в то же время видеть изменения сразу на изображении
        self._configurator = Configurator(self._renderer.watcher, self.settings, self._renderer.settings,
                                          self._constellations)
        # заданы обработчики событий для конфигуратора, которые вызываются при изменении настроек, запросе сохранения
        # изображения, а также при запросе на паузу.
        self._configurator.constellationsChangedHandler = self._apply_constellation_filter
        self._configurator.imageSaveRequestedHandler = lambda: self.viewer.image.save("sky.jpg")
        self._configurator.switchPauseRequestedHandler = self._switch_pause
        main.addLayout(self._configurator, 0, 1)

    # изменение точки обзора
    def _change_sight_vector(self, da=0, dd=0, dr=0):
        self._renderer.watcher.sight_vector += Horizontal(da, dd)
        self._renderer.watcher.up_rotation += dr
        self.setFocus()

    # обновление изображения в объекте viewer
    def _update_image(self):
        # self.viewer.width() и height - текущая ширина и высота объекта, устанавливаем их
        self._renderer.width = self.viewer.width()
        self._renderer.height = self.viewer.height()
        # генерируем новое изображение на основе объекта objects
        image = self._renderer.render(self._objects)
        # устанавливаем новое изображение
        self.viewer.image = image

    # обновление текущего времени клика
    def _on_timer_tick(self):
        if self.settings.speed != 0:
            self._update_current_time()
        self._update_image()
        self._configurator.handle()

    # обновление текущего времени
    # если speed != 0, то обновление current_time
    def _update_current_time(self):
        now = datetime.datetime.now()
        seconds_passed = (now - self._last_tick_time).total_seconds()
        self._renderer.watcher.local_time = self._renderer.watcher.local_time + datetime.timedelta(0,
                                                                                                   seconds_passed * self.settings.speed)
        self._last_tick_time = now

    # определяем небесное телескопическое зрение
    def _apply_constellation_filter(self, slctd):  # передаем координаты звезд
        stars = self._sky_sphere.get_stars(slctd)
        self._objects = stars
        self._update_image()

    # Метод получает объект события `e`. Если нажатая клавиша является одной из ключевых команд `_key_commands`,
    # то вызывается соответствующая функция из словаря `_key_commands` для выполнения команды
    def keyPressEvent(self, e):
        if e.key() in self._key_commands:
            self._key_commands[e.key()]()

    def mousePressEvent(self, QMouseEvent):
        self.setFocus()
