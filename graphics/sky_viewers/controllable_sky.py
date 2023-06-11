from datetime import datetime
from graphics.autogui.action_item import ActionItem
from graphics.autogui.bool_item import BoolItem
from graphics.autogui.field_item import FloatItem, DateTimeItem, IntItem
from graphics.autogui.gui import GUI
from graphics.sky_viewers.items.horizontal_item import HorizontalItem
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.sky import Sky
from stars.skydatabase import SkyDataBase


class ControllableSky(Sky):  # пользовательский интерфейс
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase):
        super().__init__(watcher, sky_base)

        gui = GUI("CONFIGURATOR")

        camera = gui.add(GUI("CAMERA"))  # объект камера, gui - интерфейс для
        # взаимодействия пользователя с программой с помощью клавы и мыши
        camera.add(HorizontalItem(self._renderer.watcher, "position", label="(долгота, широта)"))  # позиция
        camera.add(HorizontalItem(self._renderer.watcher, "see"))  # точка обзора
        camera.add(FloatItem(self._renderer.watcher, "up_rotation"))  # вращение вверх

        time = gui.add(GUI("DATE & TIME"))
        time.add(DateTimeItem(self._renderer.watcher, "local_time"))  # отображение текущего времени
        time.add(FloatItem(self._renderer.watcher, "star_time", True))
        time.add(FloatItem(self.settings, "second_per_second"))  # отображение скорости изменения времени
        time.add(FloatItem(self.settings, "speed_rank"))  # изменение значения скорости
        time.add(IntItem(self, "delay"))

        view = gui.add(GUI("VIEW"))
        view.add(BoolItem(self._renderer.settings, "fisheye"))
        view.add(BoolItem(self._renderer.settings, "spectral"))
        view.add(BoolItem(self._renderer.settings, "magnitude"))
        view.add(FloatItem(self._renderer.settings, "exp_factor"))
        view.add(FloatItem(self._renderer.settings, "exp_const"))
        view.add(FloatItem(self._renderer.settings, "pull"))
        view.add(BoolItem(self._renderer.settings, "up_direction"))
        view.add(BoolItem(self._renderer.settings, "see_direction"))
        # набор флажков для выбора созвездий

        gui.add(ActionItem("Save image", lambda: self.viewer.image.save("sky.jpg")))
        # возможность сохранить скрин
        gui.add(ActionItem("Pause", self._switch_pause))
        # возможность поставить на паузу
        gui.add(ActionItem("Current time", self._current_time))

        self._configurator_widget = gui.to_widget()
        self._main.addWidget(self._configurator_widget, 0, 2)
        self._gui = gui
        self._timer.timeout.connect(self._gui_tick)

        # self._timer.timeout.connect(lambda: gui.handle())
        # selected = self._constellation_filter.selected
        # self._apply_constellation_filter(selected)

        def _current_time(self):
            self._renderer.watcher.local_time = datetime.now()

    def _gui_tick(self):
        try:
            self._gui.handle()
        except Exception as e:
            print(e)

    # определяем небесное телескопическое зрение
    # определяем небесную сферу с выбранными созвездиями
    def _apply_constellation_filter(self, selected):  # передаем координаты звезд
        # stars = self._sky_sphere.get_stars(selected)
        # self._objects = stars
        # self._update_image()
        self.filter.constellations = selected
        pass

    # функция постановки на паузу/ снятия с паузы
    def _switch_pause(self):
        if self.settings.speed_rank != 0:
            self._ssr = self.settings.speed_rank
            self.settings.speed_rank = 0
        else:
            self.settings.speed_rank = self._ssr
