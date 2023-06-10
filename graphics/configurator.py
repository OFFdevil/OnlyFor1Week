from graphics.autogui.action_item import ActionItem
from graphics.autogui.bool_item import BoolItem
from graphics.autogui.field_item import FloatItem, DateTimeItem
from graphics.autogui.gui import GUI
from graphics.autogui.set_item import CheckBoxSet
from graphics.horizontal_item import HorizontalItem
from graphics.renderer.watcher import Watcher


class Configurator(GUI):  # пользовательский интерфейс
    def __init__(self, watcher: Watcher, settings, render_settings, constellations):
        super().__init__("CONFIGURATOR")
        self.constellationsChangedHandler = lambda s: s
        self.imageSaveRequestedHandler = lambda: 0
        self.switchPauseRequestedHandler = lambda: 0

        camera = self.add(GUI("CAMERA"))  # объект камера, gui - интерфейс для
        # взаимодействия пользователя с программой с помощью клавы и мыши

        camera.add(HorizontalItem(watcher, "position"))  # позиция
        camera.add(HorizontalItem(watcher, "see"))  # точка обзора
        camera.add(FloatItem(watcher, "up_rotation"))  # вращение вверх

        time = self.add(GUI("DATE & TIME"))
        time.add(DateTimeItem(watcher, "local_time"))  # отображение текущего времени
        time.add(FloatItem(settings, "speed"))  # отображение скорости изменения времени
        time.add(FloatItem(settings, "speed_rank"))  # изменение значения скорости

        other = self.add(GUI("OTHER"))
        other.add(BoolItem(render_settings, "fisheye"))  # эффект рыбьего глаза
        self.constellation_filter = other.add(
            CheckBoxSet(sorted(constellations), lambda s: self.constellationsChangedHandler(s)))

        # набор флажков для выбора созвездий

        self.add(ActionItem("Save image", lambda: self.imageSaveRequestedHandler()))
        # возможность сохранить скрин
        self.add(ActionItem("Pause", lambda: self.switchPauseRequestedHandler()))
        # возможность поставить на паузу
