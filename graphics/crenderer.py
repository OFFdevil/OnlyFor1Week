import datetime

import re

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

from geometry.avector import Horizontal
from graphics.autogui.bool_item import BoolItem
from graphics.autogui.field_item import FloatItem, FieldItem, DateTimeItem
from graphics.autogui.gui import GUI
from graphics.autogui.set_item import CheckBoxSet
from graphics.image_viewer import ImageViewer
from graphics.renderer.camera import Camera
from graphics.renderer.renderer import Renderer
from graphics.renderer.settings import ControllableRenderSettings
from graphics.renderer.watcher import Watcher
from stars.skybase import SkyBase


# определяем класс HorizontalItem, который наследуется от FieldItem
# содержит методы для парсинга строк и инициализации объектов
class HorizontalItem(FieldItem):
    # TODO: move to Horizontal
    @staticmethod
    def parse_str(s, regexp):  # метод получает на вход строку и регулярное выражение
        # далее используем это рег выражение для поиска и извлечения значений из строки
        match = regexp.match(s)
        if match is None:  # если строка не соответствует шаблону, то выбрасываем исключение
            print("!")
            raise ValueError()
        groups = match.groupdict()
        if (not ("a" in groups)) or (not ("d" in groups)):
            # если значения не извлечь из строки, то также выбрасываем исключение
            print("!!")
            raise ValueError()
        print(groups["a"], groups["d"])
        return Horizontal(float(groups["a"]), float(groups["d"]))

    def __init__(self, obj: object, fname: str):  # принимаем объект и поле объекта
        pregex = "^\((?P<a>[+-]?[\d.]+?), ?(?P<d>[+-]?[\d.]+?)\)$"
        cpregexp = re.compile(pregex)
        builder = str
        parser = lambda s: HorizontalItem.parse_str(s, cpregexp)  # использует лямбда-функцию parser для парсинга
        # значений из строки
        super().__init__(obj, fname, builder, parser)


# создаем класс ControllableRenderer, который наследуется от QtWidgets.QWidget
# содержит методы для инициализации экрана рендеринга с небесной сферой и камерой, управления и перерисовкой
class ControllableRenderer(QtWidgets.QWidget):
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

            QtCore.Qt.Key_Equal: lambda: self._change_zoom(1.5),
            QtCore.Qt.Key_Minus: lambda: self._change_zoom(2 / 3)
        }

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(1000 / self.settings.fps)
        self._timer.timeout.connect(self._on_timer_tick)

        self._constellations = sky_sphere.constellations

        self._cmodel = QStandardItemModel()
        self._create_configurator()
        self.setFocus()

        self._last_tick_time = datetime.datetime.now()
        self._on_timer_tick()  # вызывается при истечении времени таймера и обновляет содержимое окна
        self._timer.start()

    def _create_configurator(self):
        # создаем окно с конфигуратором
        main = QtWidgets.QGridLayout()
        self.setLayout(main)
        self.viewer = ImageViewer()
        main.addWidget(self.viewer, 0, 0)
        main.setColumnStretch(0, 1)

        configurator = QtWidgets.QVBoxLayout()

        self.gui = GUI("CONFIGURATOR")
        configurator.addLayout(self.gui)

        # окно разбито на несколько разделов: CAMERA, DATE & TIME, OTHER
        camera = self.gui.add(GUI("CAMERA"))

        # пользователь в разделе CAMERA может настроить долготу, широту, точка обзора, угол поворота
        camera.add(HorizontalItem(self._renderer.watcher, "position"))
        camera.add(HorizontalItem(self._renderer.watcher, "sight_vector"))
        camera.add(FloatItem(self._renderer.watcher, "up_rotation"))

        # пользователь может настроить дату, время, скорость и ранг скорости
        time = self.gui.add(GUI("DATE & TIME"))
        time.add(DateTimeItem(self._renderer.watcher, "local_time"))
        time.add(FloatItem(self.settings, "speed"))
        time.add(FloatItem(self.settings, "speed_rank"))

        # пользователь может выбрать одно или несколько созвездий для фильтрации на карте
        other = self.gui.add(GUI("OTHER"))
        other.add(BoolItem(self._renderer.settings, "fisheye"))
        other.add(CheckBoxSet(sorted(self._constellations), lambda s: self._apply_constellation_filter(s)))

        main.addLayout(configurator, 0, 1)

    def _change_zoom(self, d_zoom):
        d_zoom = max(d_zoom,
                     self._renderer.watchersight_radius / 90)  # сравниваем d_zoom с значением радиуса обзора камеры/90
        self.settings.zoom = self.settings.zoom * d_zoom
        # присваиваем обновленное значение
        self._renderer.watcher.sight_radius = self._renderer.watcher.sight_radius / d_zoom
        self._zoom_widget.setText(str(self._renderer.watcher.sight_radius))
        self.setFocus()

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
        self.gui.handle()

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
