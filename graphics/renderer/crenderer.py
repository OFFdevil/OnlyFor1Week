import datetime
from PyQt5 import QtCore

from PyQt5 import QtWidgets

from geometry.avector import Horizontal
from graphics.renderer.camera import Camera
from graphics.renderer.renderer import Canvas
from graphics.renderer.settings import ControllableRenderSettings
from graphics.renderer.ui import create_float_widget, create_datetime_widget
from stars.skybase import SkyBase


# создаем класс ControllableRenderer, который наследуется от QtWidgets.QWidget
# содержит методы для инициализации экрана рендеринга с небесной сферой и камерой, управления и перерисовкой
class ControllableRenderer(QtWidgets.QWidget):
    def __init__(self, camera: Camera, sky_sphere: SkyBase, start_time: datetime.datetime):
        super().__init__()

        # задаем все методы
        self._canvas = Canvas(camera, start_time)
        self._sky_sphere = sky_sphere
        self.settings = ControllableRenderSettings()
        self._magnitude_lower_th = 6
        self._magnitude_upper_th = 0
        self._datetime_format = "%d.%m.%Y %H:%M:%S"
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

        self._init_ui()
        self.setFocus()

        self._last_tick_time = datetime.datetime.now()
        self._apply_constellation_filter()
        self._on_timer_tick()  # вызывается при истечении времени таймера и обновляет содержимое окна
        self._timer.start()

    def _init_ui(self):
        # создание объекта layout, устанавливаем его как основной макет для текущего виджета
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        # объект canvas с координатами (0, 0) в layout
        layout.addWidget(self._canvas, 0, 0)
        # устанавливаем гибкий размер для столбца с индексом 0 в layout
        layout.setColumnStretch(0, 1)

        # добавляем объект tools_layout в ячейку с координатами (0, 1) в layout
        tools_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(tools_layout, 0, 1)

        # добавили time_zone в tools_layout
        time_zone = QtWidgets.QGridLayout()
        tools_layout.addLayout(time_zone)

        # добавляем виджеты времени и скорости в time_zone
        self._datetime_widget = create_datetime_widget(self._canvas, "datetime", self._datetime_format)
        time_zone.addWidget(self._datetime_widget)

        self._speed_widget = create_float_widget(self.settings, "speed")
        time_zone.addWidget(self._speed_widget)

        # добавляем объект constellation_zone (горизонтальный блок виджетов, в который будут добавлены другие)
        constellation_zone = QtWidgets.QHBoxLayout()
        tools_layout.addLayout(constellation_zone)

        # создаем элементы интерфейса - выпадающий список для выбора созвездий, несколько значений для настройки
        # камеры и метки, чтобы указать, что каждый из элементов управляет широтой, долготой, радиусом
        self._constellation_widget = QtWidgets.QComboBox()
        self._constellation_widget.addItem('')
        self._constellation_widget.addItems(sorted(self._sky_sphere.get_constellations()))
        self._constellation_widget.activated.connect(self.setFocus)
        self._constellation_widget.activated.connect(self._apply_constellation_filter)
        # все виджеты добавляются в вертикальной блок
        constellation_zone.addWidget(self._constellation_widget)

        camera_layout = QtWidgets.QGridLayout()
        tools_layout.addLayout(camera_layout)

        # создаем элемент долгота, в нулевой столбец и нулевую строку
        camera_layout.addWidget(QtWidgets.QLabel('long:'), 0, 0)
        self._longitude_widget = create_float_widget(self._canvas.camera, "longitude")
        camera_layout.addWidget(self._longitude_widget, 0, 1)

        # создаем элемент ширина
        camera_layout.addWidget(QtWidgets.QLabel('lat:'), 1, 0)
        self._latitude_widget = create_float_widget(self._canvas.camera, "latitude")
        camera_layout.addWidget(self._latitude_widget, 1, 1)

        # создаем элемент радиус
        camera_layout.addWidget(QtWidgets.QLabel('radius:'), 2, 0)
        self._zoom_widget = QtWidgets.QLineEdit(str(self._canvas.camera.sight_radius))
        self._zoom_widget.editingFinished.connect(  # когда пользователь закончит ввод текста и уберет фокус с
            # виджета, то вызовется lambda
            lambda: self._change_zoom(  # изменится радиус обзора камеры
                self._canvas.camera.sight_radius / float(self._zoom_widget.text())
            )
        )

        # создаем элемент угол и далее аналогично пред пункту
        camera_layout.addWidget(self._zoom_widget, 2, 1)
        camera_layout.addWidget(QtWidgets.QLabel('angle:'), 3, 0)
        self._sight_vector_azimuth = QtWidgets.QLineEdit(str(self._canvas.camera.sight_vector().alpha))
        self._sight_vector_azimuth.editingFinished.connect(
            lambda: self._set_sight_vector(
                float(self._sight_vector_azimuth.text()),
                self._canvas.camera.sight_vector().delta
            )
        )
        camera_layout.addWidget(self._sight_vector_azimuth, 3, 1)

        # создаем элемент delta, размещаем в 4 строке и 0 столбце
        camera_layout.addWidget(QtWidgets.QLabel('delta:'), 4, 0)
        self._sight_vector_altitude = QtWidgets.QLineEdit(str(self._canvas.camera.sight_vector().delta))
        self._sight_vector_altitude.editingFinished.connect(  # когда пользователь закончит редактирование этого поля,
            # то будет вызван метод _set_sight_vector
            lambda: self._set_sight_vector(
                self._canvas.camera.sight_vector().alpha,
                float(self._sight_vector_altitude.text())
            )
        )
        camera_layout.addWidget(self._sight_vector_altitude, 4, 1)

        tools_layout.addWidget(QtWidgets.QWidget())
        tools_layout.setStretch(7, 1)

    def _change_zoom(self, d_zoom):
        d_zoom = max(d_zoom,
                     self._canvas.camera.sight_radius / 90)  # сравниваем d_zoom с значением радиуса обзора камеры/90
        self.settings.zoom = self.settings.zoom * d_zoom
        # присваиваем обновленное значение
        self._canvas.camera.sight_radius = self._canvas.camera.sight_radius / d_zoom
        self._zoom_widget.setText(str(self._canvas.camera.sight_radius))
        self.setFocus()

    # изменение точки обзора
    def _change_sight_vector(self, da=0, dd=0, dr=0):
        self._canvas.camera.sight_vector += Horizontal(da, dd)
        self._canvas.camera.up_rotation += dr
        self.setFocus()

    # обновление текущего времени клика
    def _on_timer_tick(self):
        if self.settings.speed != 0:
            self._update_current_time()
        self._canvas.repaint()

    # обновление текущего времени
    def _update_current_time(self):
        now = datetime.datetime.now()
        seconds_passed = (now - self._last_tick_time).total_seconds()
        self._canvas.datetime += datetime.timedelta(0, seconds_passed * self.settings.speed)
        self._last_tick_time = now
        self._datetime_widget.setText(self._canvas.datetime.strftime(self._datetime_format))

    # Метод класса, который применяет фильтр по созвездию к звездам на небесной сфере, представленным в `stars`. Он
    # принимает `constellation` в качестве параметра и фильтрует звезды, выбирая только те, которые принадлежат
    # указанному созвездию. Затем он обновляет `self._canvas.objects`, чтобы отобразить только отфильтрованные звезды
    # на экране
    def _apply_constellation_filter(self):
        stars = self._sky_sphere.get_visible_stars(self._canvas.camera, self._canvas.datetime)
        constellation = self._constellation_widget.currentText()
        if constellation != '':
            stars = [star for star in stars if star.constellation == constellation]
        self._canvas.objects = stars
        self._canvas.repaint()

    # Метод получает объект события `e`. Если нажатая клавиша является одной из ключевых команд `_key_commands`,
    # то вызывается соответствующая функция из словаря `_key_commands` для выполнения команды
    def keyPressEvent(self, e):
        if e.key() in self._key_commands:
            self._key_commands[e.key()]()

    def mousePressEvent(self, QMouseEvent):
        self.setFocus()
