from datetime import datetime
from graphics.autogui.action_item import ActionItem
from graphics.autogui.bool_item import BoolItem
from graphics.autogui.field_item import FloatItem, DateTimeItem, IntItem
from graphics.autogui.gui import GUI
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.items.horizontal_item import HorizontalItem
from graphics.sky_viewers.sky import Sky
from stars.filter import Filter
from stars.skydatabase import SkyDataBase
from utility import try_or_print


class ControllableSky(Sky):
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase, selector: Filter):
        super().__init__(watcher, sky_base, selector)

        gui = GUI("CONFIGURATOR")

        camera = gui.add(GUI("CAMERA"))
        camera.add(HorizontalItem(self.renderer.watcher, "position", label="(longitude, latitude)"))
        camera.add(HorizontalItem(self.renderer.watcher, "see"))
        camera.add(HorizontalItem(self.renderer.watcher, "up", ro=True))
        camera.add(FloatItem(self.renderer.watcher, "up_rotation"))

        time = gui.add(GUI("DATE & TIME"))
        time.add(DateTimeItem(self.renderer.watcher, "local_time"))
        time.add(FloatItem(self.renderer.watcher, "star_time", True))
        time.add(FloatItem(self.settings, "second_per_second"))
        time.add(FloatItem(self.settings, "speed_rank"))
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

        gui.add(ActionItem("Save image", self.viewer.save_to_file))
        gui.add(ActionItem("Pause", self.switch_pause))
        gui.add(ActionItem("Current time", self.set_current_time))

        self._configurator_widget = gui
        self._main.addWidget(self._configurator_widget, 0, 2)
        self._gui = gui
        self.timer.timeout.connect(self._gui_tick)

    def set_current_time(self):
        self.renderer.watcher.local_time = datetime.now()

    @try_or_print
    def _gui_tick(self):
        self._gui.handle()

    def _apply_constellation_filter(self, selected):
        self.filter.constellations = selected

    def switch_pause(self):
        if self.settings.speed_rank != 0:
            self._ssr = self.settings.speed_rank
            self.settings.speed_rank = 0
        else:
            self.settings.speed_rank = self._ssr
