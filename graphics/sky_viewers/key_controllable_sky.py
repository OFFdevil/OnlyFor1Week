from PyQt5.QtCore import Qt
from geometry.horizontal import Horizontal
from graphics.sky_viewers.filterable_sky import FilterableSky
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.key_processor import KeyProcessor
from stars.skydatabase import SkyDataBase
from stars.filter import Filter
from utility import try_or_print


class KeyControllableSky(FilterableSky):
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase, selector: Filter):
        super().__init__(watcher, sky_base, selector)

        self.setFocus()

        self._configurator_widget.setVisible(False)
        # прописывание команд, которые выполняются при нажатии клавиш движение вверх, вниз, вправо, влево, пауза,
        # сохранение изображения, открытие меню и изображения на полный экран
        pr = self._key_processor = KeyProcessor()
        pr.should_be_called(self._look_around) \
            .when_pressed(Qt.Key_W).with_arguments(0, 2, 0) \
            .when_pressed(Qt.Key_A).with_arguments(2, 0, 0) \
            .when_pressed(Qt.Key_S).with_arguments(0, -2, 0) \
            .when_pressed(Qt.Key_D).with_arguments(-2, 0, 0) \
            .when_pressed(Qt.Key_Q).with_arguments(0, 0, 2) \
            .when_pressed(Qt.Key_E).with_arguments(0, 0, -2)
        pr.should_be_called(self.switch_pause).when_pressed(Qt.Key_Space)
        pr.should_be_called(self.switch_menu).when_pressed(Qt.Key_M)
        pr.should_be_called(self.switch_filter).when_pressed(Qt.Key_N)
        pr.should_be_called(self.switch_full_screen).when_pressed(Qt.Key_F)
        pr.should_be_called(self.viewer.save_to_file).when_pressed(Qt.Key_I)
        pr.should_be_called(self.close).when_pressed(Qt.Key_Escape)
        pr.should_be_called(self.rerender).when_pressed(Qt.Key_R)

    # функция открытия на полный экран
    def switch_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    # функция открытия меню
    def switch_menu(self):
        self._configurator_widget.setVisible(not self._configurator_widget.isVisible())

    def switch_filter(self):  # изменение состояния виджета(если бы видимым, станет невидимым и наоборот)
        self._filter_widget.setVisible(not self._filter_widget.isVisible())

    # функция сдвигающая небо в нужную сторону (в зависимости от клавиш)
    @try_or_print
    def _look_around(self, *delta):
        da, dh, dr = delta
        self.renderer.watcher.up_rotation += dr
        if abs(self.renderer.watcher.see.h + dh) > 90:
            return
        self.renderer.watcher.see += Horizontal(da, dh)

    # Метод получает объект события `e`. Если нажатая клавиша является одной из ключевых команд `_key_commands`,
    # то вызывается соответствующая функция из словаря `_key_commands` для выполнения команды

    def keyPressEvent(self, e):
        self._key_processor.execute(e.key())

    def mousePressEvent(self, QMouseEvent):
        self.setFocus()
