from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter

from geometry.equatorial import Equatorial
from geometry.horizontal import Horizontal
from graphics.renderer.projector import Projector, ProjectedStar
from graphics.renderer.utility import try_or_print
from graphics.renderer.watcher import Watcher
from stars.star import Star


# в целом класс отвечает за прорисовку неба и звезд, содержит в себе несколько методов для рисования звезд на виджете
class Renderer(Projector):
    def __init__(self, watcher: Watcher):
        super().__init__(watcher)
        self._buffer = QImage(QSize(0, 0), QImage.Format_RGB32)  # создаем объект размером 0*0
        self._painter = QPainter()

        # ширина и высота изображения, заданного для отрисовки
        self._width = 0
        self._height = 0
        self.width = 1920
        self.height = 1080
        # self._distortion = fisheye_distortion  # хранит значение искажения в съемке с широкоугольной камеры

    @property
    def width(self):  # геттер ширины
        return self._width

    @property
    def height(self):  # геттер ширины
        return self._height

    @width.setter  # сеттер ширины
    def width(self, value):
        if value != self.width:  # если новое значение отличается от старого, то устанавливает новое и создает буфер
            # изображения, используя стандартный формат
            self._width = value
            self.centre = (self._width // 2, self._height // 2)
            self._buffer = QImage(QSize(self.width, self.height), QImage.Format_RGB32)

    @height.setter  # сеттер высоты, аналогично для нее
    def height(self, value):
        if value != self.height:
            self._height = value
            self.centre = (self._width // 2, self._height // 2)
            self._buffer = QImage(QSize(self.width, self.height), QImage.Format_RGB32)

    # используем значение параметра fisheye, по нему определяем нужно ли имитировать эффект съёмки широкоугольной
    # камеры или нет
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
        self.settings.apply_color("sky", self._painter)  # устанавливаем цвет
        self._painter.drawRect(0, 0, self.width,
                               self.height)  # рисуем прямоугольник с координатами (0, 0) с данной высотой и шириной

    # def _draw_up(self):
    #     self._draw_object(Horizontal(0, 90), None)
    #     self._draw_object(Horizontal(0, 90), None)

    def _draw_compass(self):  # отрисовка компаса
        # n = self._draw_latidude_depencing_point(Equatorial(0, 90), 'north', -3)
        # s = self._draw_latidude_depencing_point(Equatorial(0, -90), 'south', -3)
        # try:
        #     self.settings.apply_color('north', self._painter)
        #     self._painter.drawLine(n.cx, n.cy, self.centre[0], self.centre[1])
        #     self.settings.apply_color('south', self._painter)
        #     self._painter.drawLine(self.centre[0], self.centre[1], s.cx, s.cy)
        # except Exception as e:
        #     print(e)
        self._draw_point_and_direction(Equatorial(0, 90), 'north', -3, True)
        self._draw_point_and_direction(Equatorial(0, -90), 'south', -3, True)

    def _draw_latidude_depencing_point(self, pos: Equatorial, color, size):
        # рисует звезду в положении, которое зависит от ее широты
        # основывается на положении наблюдателя
        self.settings.apply_color(color, self._painter)
        lat = pos.to_horizontal_with_latitude(self.watcher.position.h)
        p_lat = self.project_star(lat, Star(pos, '', size, '', ''), True)
        if p_lat is not None and p_lat.in_eye:  # если звезда в поле зрения, то рисуем ее
            self._draw_object(p_lat, False)
        return p_lat  # возвращает проекцию звезды на экране

    @try_or_print
    def _draw_see_points(self):  # отвечает за отрисовку точки северного полюса
        # if self.watcher.position is not None:
        #     # находим точку на небесной сферической системе, которая соответствует заданному
        #     # небесному объекту
        #     forward = self.project_star(self.watcher.position, Star(Equatorial(0, 90), '', -1, '', ''), True)
        #     upborder = self.project_star(Horizontal(0, 90), Star(Equatorial(0, 90), '', -1, '', ''), True)
        #     downborder = self.project_star(Horizontal(0, -90), Star(Equatorial(0, 90), '', -1, '', ''), True)
        #     self.settings.apply_color('up', self._painter)
        #     if forward.in_eye:
        #         self._draw_object(forward, False)
        #     self._painter.drawLine(self.centre[0], self.centre[1], forward.cx, forward.cy)
        #     self.settings.apply_color('up_border', self._painter)
        #     if upborder.in_eye:
        #         self._draw_object(upborder, False)
        #     self._painter.drawLine(self.centre[0], self.centre[1], upborder.cx, upborder.cy)
        #     if downborder.in_eye:
        #         self._draw_object(downborder, False)
        #     self._painter.drawLine(self.centre[0], self.centre[1], downborder.cx, downborder.cy)
        self._draw_point_and_direction(self.watcher.position, 'up', -1, False)
        self._draw_point_and_direction(Equatorial(0, 90), 'up_border', -1, False)
        self._draw_point_and_direction(Equatorial(0, -90), 'up_border', -1, False)

    def _draw_screen_centre(self):
        self.settings.apply_color('see', self._painter)  # устанавливаем цвет
        diameter = self._get_size(-2)
        diameter, _ = self.distortion(diameter, 0, self.watcher.radius, 0)  # считаем диаметр на основании
        # верхнего угла, далее рисуем круг
        x, y = self.centre[0] - diameter // 2, self.centre[
            1] - diameter // 2  # по координатам центра и диаметру находим коорд левого
        # верхнего угла, далее рисуем круг
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
