from graphics.autogui.gui import GUI
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.controllable_sky import ControllableSky
from graphics.sky_viewers.items.filter_item import FilterItem
from stars.skydatabase import SkyDataBase


# класс, отвечающий за отображение только выбранных пользователем созвездий
class FiltrableSky(ControllableSky):
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase):
        super().__init__(watcher, sky_base)

        # создаем объект, используя переданный фильтр, созвездия и функцию, выбранных созвездий
        gui = FilterItem(self.filter, self._available_constellations, self._apply_constellation_filter)
        self._filter_widget = gui.to_widget()
        # создаем объект, делаем его видимым и добавляем в главное окно
        self._filter_widget.setVisible(False)
        self._main.addWidget(self._filter_widget, 0, 1)

        # будем обновлять список созвездий с учетом заданных фильтров
        self._timer.timeout.connect(gui.handle)
