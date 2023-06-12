from datetime import datetime
from graphics.autogui.action_item import ActionItem
from graphics.autogui.bool_item import BoolItem
from graphics.autogui.field_item import FloatItem, DateTimeItem, IntItem
from graphics.autogui.gui import GUI
from graphics.sky_viewers.items.horizontal_item import HorizontalItem
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.sky import Sky
from stars.filter import Filter
from stars.skydatabase import SkyDataBase


class ControllableSky(Sky):  # пользовательский интерфейс
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase, filter: Filter):
        super().__init__(watcher, sky_base, filter)

        gui = GUI("CONFIGURATOR")

        camera = gui.add(GUI("CAMERA"))  # объект камера, gui - интерфейс для
        # взаимодействия пользователя с программой с помощью клавиатуры и мыши
        camera.add(HorizontalItem(self.renderer.watcher, "position", label="(долгота, широта)"))  # позиция
        camera.add(HorizontalItem(self.renderer.watcher, "see"))  # точка обзора
        camera.add(HorizontalItem(self.renderer.watcher, "up", ro=True))
        camera.add(FloatItem(self.renderer.watcher, "up_rotation"))  # вращение вверх

        time = gui.add(GUI("DATE & TIME"))
        time.add(DateTimeItem(self.renderer.watcher, "local_time"))  # отображение текущего времени
        time.add(FloatItem(self.renderer.watcher, "star_time", True))
        time.add(FloatItem(self.settings, "second_per_second"))  # отображение скорости изменения времени
        time.add(FloatItem(self.settings, "speed_rank"))  # изменение значения скорости
        time.add(IntItem(self, "delay"))
        time.add(IntItem(self, "_rdelay"))

        view = gui.add(GUI("VIEW"))
        view.add(BoolItem(self.renderer, "settings.fisheye"))
        view.add(IntItem(self, "forecast_step"))
        view.add(BoolItem(self.renderer, "settings.spectral"))
        view.add(BoolItem(self.renderer, "settings.magnitude"))
        view.add(FloatItem(self.renderer, "settings.exp_factor"))
        view.add(FloatItem(self.renderer, "settings.exp_const"))
        view.add(FloatItem(self.renderer, "settings.pull"))
        view.add(BoolItem(self.renderer, "settings.see_points"))
        view.add(BoolItem(self.renderer, "settings.screen_centre"))
        view.add(BoolItem(self.renderer, "settings.compass"))
        # набор флажков для выбора созвездий

        gui.add(ActionItem("Save image", self.viewer.save_to_file))
        # возможность сохранить скрин
        gui.add(ActionItem("Pause", self.switch_pause))
        # возможность поставить на паузу
        gui.add(ActionItem("Current time", self.set_current_time))

        self._configurator_widget = gui
        self._main.addWidget(self._configurator_widget, 0, 2)
        self._gui = gui
        self.timer.timeout.connect(self._gui_tick)

        # self._timer.timeout.connect(lambda: gui.handle())
        # selected = self._constellation_filter.selected
        # self._apply_constellation_filter(selected)

    def current_time(self):
        self.renderer.watcher.local_time = datetime.now()

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
    def switch_pause(self):
        if self.settings.speed_rank != 0:
            self._ssr = self.settings.speed_rank
            self.settings.speed_rank = 0
        else:
            self.settings.speed_rank = self._ssr
