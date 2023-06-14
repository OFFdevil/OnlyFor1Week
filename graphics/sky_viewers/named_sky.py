from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QToolTip
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.mouse_controllable_sky import MouseControllableSky
from stars.skydatabase import SkyDataBase
from stars.filter import Filter


class NamedSky(MouseControllableSky):
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase, selector: Filter):
        super().__init__(watcher, sky_base, selector)
        self.timer.timeout.connect(self._show_tip)
        self._last_mouse = (0, 0)
        self._last_star = None

    def _show_tip(self,
                  it: bool = False):
        self._last_mouse = self._mouse_pos
        star = self.renderer.find_star(*self._mouse_pos, 1)
        if star is not None:
            if self._last_star is None or star.star != self._last_star or it:
                self._last_star = star.star
                QToolTip.showText(QPoint(*self._mouse_gpos), str(star.star))
        else:
            QToolTip.hideText()
            self._last_star = None
