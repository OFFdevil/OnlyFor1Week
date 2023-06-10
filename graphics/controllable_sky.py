from graphics.autogui.action_item import ActionItem
from graphics.autogui.bool_item import BoolItem
from graphics.autogui.field_item import FloatItem, DateTimeItem
from graphics.autogui.gui import GUI
from graphics.autogui.set_item import CheckBoxSet
from graphics.horizontal_item import HorizontalItem
from graphics.renderer.watcher import Watcher
from graphics.sky import Sky
from stars.skydatabase import SkyDataBase


class ControllableSky(Sky):  # пользовательский интерфейс
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase):
        super().__init__(watcher, sky_base)

        gui = GUI("CONFIGURATOR")

        camera = gui.add(GUI("CAMERA"))  # объект камера, gui - интерфейс для
        # взаимодействия пользователя с программой с помощью клавы и мыши
        camera.add(HorizontalItem(self._renderer.watcher, "position"))  # позиция
        camera.add(HorizontalItem(self._renderer.watcher, "see"))  # точка обзора
        camera.add(FloatItem(self._renderer.watcher, "up_rotation"))  # вращение вверх

        time = gui.add(GUI("DATE & TIME"))
        time.add(DateTimeItem(self._renderer.watcher, "local_time"))  # отображение текущего времени
        time.add(FloatItem(self._renderer.watcher, "star_time", True))
        time.add(FloatItem(self.settings, "speed"))  # отображение скорости изменения времени
        time.add(FloatItem(self.settings, "speed_rank"))  # изменение значения скорости

        other = gui.add(GUI("OTHER"))
        other.add(BoolItem(self._renderer.settings, "fisheye"))  # эффект рыбьего глаза
        self._constellation_filter = other.add(
            CheckBoxSet(sorted(self._available_constellations), self._apply_constellation_filter))

        # набор флажков для выбора созвездий

        gui.add(ActionItem("Save image", lambda: self.viewer.image.save("sky.jpg")))
        # возможность сохранить скрин
        gui.add(ActionItem("Pause", self._switch_pause))
        # возможность поставить на паузу

        self._configurator_widget = gui.to_widget()
        self._main.addWidget(self._configurator_widget, 0, 1)

        self._timer.timeout.connect(lambda: gui.handle())

        selected = self._constellation_filter.selected
        self._apply_constellation_filter(selected)

    # определяем небесное телескопическое зрение

    def _apply_constellation_filter(self, slctd):  # передаем координаты звезд
        stars = self._sky_sphere.get_stars(slctd)
        self._objects = stars
        self._update_image()

    # функция постановки на паузу
    def _switch_pause(self):
        if self._timer.isActive():
            self._timer.stop()
        else:
            self._timer.start()
