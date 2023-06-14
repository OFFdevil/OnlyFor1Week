from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter
from geometry.equatorial import Equatorial
from geometry.horizontal import Horizontal
from graphics.renderer.projector import Projector, ProjectedStar
from utility import try_or_print
from graphics.renderer.watcher import Watcher
from stars.star import Star


class Renderer(Projector):
    def __init__(self, watcher: Watcher):
        super().__init__(watcher)
        self._buffer = QImage(QSize(0, 0), QImage.Format_RGB32)
        self._painter = QPainter()
        self._width = 0
        self._height = 0
        self.width = 1920
        self.height = 1080

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @width.setter
    def width(self, value):
        if value != self.width:
            self._width = value
            self.centre = (self._width // 2, self._height // 2)
            self._buffer = QImage(QSize(self.width, self.height), QImage.Format_RGB32)

    @height.setter
    def height(self, value):
        if value != self.height:
            self._height = value
            self.centre = (self._width // 2, self._height // 2)
            self._buffer = QImage(QSize(self.width, self.height), QImage.Format_RGB32)

    def render(self, stars: list, forecast: bool):
        self._painter.begin(self._buffer)
        self.clear_buffer()
        for o in self.project(stars, forecast):
            self._draw_object(o)
        if self.settings.see_points:
            self._draw_see_points()
        if self.settings.screen_centre:
            self._draw_screen_centre()
        if self.settings.compass:
            self._draw_compass()
        self._painter.end()
        return self._buffer

    def clear_buffer(self):
        self.settings.apply_color("sky", self._painter)
        self._painter.drawRect(0, 0, self.width, self.height)

    def _draw_compass(self):
        self._draw_point_and_direction(Equatorial(0, 90), 'north', -3, True)
        self._draw_point_and_direction(Equatorial(0, -90), 'south', -3, True)

    @try_or_print
    def _draw_see_points(self):
        self._draw_point_and_direction(self.watcher.position, 'up', -1, False)
        self._draw_point_and_direction(Equatorial(0, 90), 'up_border', -1, False)
        self._draw_point_and_direction(Equatorial(0, -90), 'up_border', -1, False)

    def _draw_screen_centre(self):
        self.settings.apply_color('see', self._painter)
        diameter = self._get_size(-2)
        diameter, _ = self.distortion(diameter, 0, self.watcher.radius, 0)
        x, y = self.centre[0] - diameter // 2, self.centre[
            1] - diameter // 2
        self._painter.drawEllipse(int(x), int(y), int(diameter), int(diameter))

    def _draw_point_and_direction(self, pos: Equatorial, color, size, apply_latitude):
        self.settings.apply_color(color, self._painter)
        if apply_latitude:
            horizontal = pos.to_horizontal_with_latitude(self.watcher.position.h)
        elif isinstance(pos, Equatorial):
            horizontal = Horizontal(pos.a, pos.d)
        else:
            horizontal = pos
        p_lat = self.project_star(horizontal, Star(pos, '', size, '', ''), True)
        if p_lat is not None and p_lat.in_eye:
            self._draw_object(p_lat, False)
        self._painter.drawLine(int(p_lat.cx), int(p_lat.cy), int(self.centre[0]), int(self.centre[1]))

    def _draw_object(self, pstar: ProjectedStar, with_color=True):
        if with_color:
            if self.settings.spectral:
                self.settings.apply_color(pstar.star.spectral_class, self._painter)
            else:
                self.settings.apply_color('star', self._painter)
        x, y = pstar.cx - pstar.diameter // 2, pstar.cy - pstar.diameter // 2
        self._painter.drawEllipse(int(x), int(y), int(pstar.diameter), int(pstar.diameter))
