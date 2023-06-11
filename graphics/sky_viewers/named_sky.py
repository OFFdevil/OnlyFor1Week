from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QToolTip

from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.mouse_controllable_sky import MouseControllableSky
from stars.skydatabase import SkyDataBase


# файл, отвечающий за всплывающие подсказки(наводим на звезду, получаем ее информацию)
class NamedSky(MouseControllableSky):
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase):
        super().__init__(watcher, sky_base)
        self._timer.timeout.connect(self._show_tip)
        self._last_mouse = (0, 0)
        self._last_star = None

    def _show_tip(self,
                  it: bool = False):  # функция показывающая всплывающую информацю про звезду, если на нее наведена мышь
        self._last_mouse = self._mouse_pos
        star = self._renderer.find_star(*self._mouse_pos, 1)
        if star is not None:
            if self._last_star is None or star.star != self._last_star or it:
                self._last_star = star.star
                QToolTip.showText(QPoint(*self._mouse_gpos), str(star.star))  # выводим информацию про звезду
        else:  # если не наведена, скрываем подсказку
            QToolTip.hideText()
            self._last_star = None
