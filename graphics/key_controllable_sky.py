import sys
from PyQt5.QtCore import Qt
from geometry.horizontal import Horizontal
from graphics.controllable_sky import ControllableSky
from graphics.renderer.watcher import Watcher
from graphics.utility import KeyProcessor
from stars.skydatabase import SkyDataBase


class KeyControllableSky(ControllableSky):
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase):
        super().__init__(watcher, sky_base)

        self.setFocus()

        self._configurator_widget.setVisible(False)
        # прописывание команд, которые выполняются при нажатии клавиш движение вверх, вниз, вправо, влево, пауза,
        # сохранение изображения, открытие меню и изображения на полный экран
        self._key_processor = KeyProcessor() \
            .register("look", self._look_around) \
            .bind(Qt.Key_W, 'look', (0, 2, 0)) \
            .bind(Qt.Key_A, 'look', (2, 0, 0)) \
            .bind(Qt.Key_S, 'look', (0, -2, 0)) \
            .bind(Qt.Key_D, 'look', (-2, 0, 0)) \
            .bind(Qt.Key_Q, 'look', (0, 0, 2)) \
            .bind(Qt.Key_E, 'look', (0, 0, -2)) \
            .register("pause", self._switch_pause) \
            .bind(Qt.Key_Space, 'pause') \
            .register("menu", self._switch_menu) \
            .bind(Qt.Key_M, 'menu') \
            .register("image", self.viewer.save_to_file) \
            .bind(Qt.Key_I, "image") \
            .register("full_screen", self._switch_full_screen) \
            .bind(Qt.Key_F, "full_screen") \
            .register("exit", lambda: sys.exit(0)) \
            .bind(Qt.Key_Escape, "exit")

    # функция открытия на полный экран
    def _switch_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    # функция открытия меню
    def _switch_menu(self):
        self._configurator_widget.setVisible(not self._configurator_widget.isVisible())

    # функция сдвигающая небо в нужную сторону (в зависимости от клавиш)
    def _look_around(self, *delta):
        da, dd, dr = delta
        self._renderer.watcher.up_rotation += dr
        self._renderer.watcher.see += Horizontal(da, dd)

    # Метод получает объект события `e`. Если нажатая клавиша является одной из ключевых команд `_key_commands`,
    # то вызывается соответствующая функция из словаря `_key_commands` для выполнения команды

    def keyPressEvent(self, e):
        self._key_processor.execute(e.key())

    def mousePressEvent(self, QMouseEvent):
        self.setFocus()
