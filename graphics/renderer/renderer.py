from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter

from graphics.renderer.projector import Projector, ProjectedStar
from geometry.equatorial import Equatorial

from graphics.renderer.watcher import Watcher


# в целом класс отвечает за прорисовку неба и звезд, содержит в себе несколько методов для рисования звезд на виджете
class Renderer(Projector):
    def __init__(self, watcher: Watcher):
        super().__init__(watcher)
        self._buffer = QImage(QSize(0, 0), QImage.Format_RGB32)  # создаем объект размером 0*0
        self._painter = QPainter()

        # ширина и высота изображения, заданного для отрисовки
        self._width = 0
        self._height = 0
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
    def render(self, stars: list):
        try:
            self._painter.begin(self._buffer)
            self._draw_background()
            for o in self.project(stars):
                self._draw_object(o)
            # if self.settings.up_direction:
            #    self._draw_up()
            if self.settings.see_direction:
                self._draw_see()
            self._painter.end()
            return self._buffer
        except Exception as ex:
            print(ex)

    # рисуем звезду по данным из ProjectedStar
    def _draw_object(self, pstar: ProjectedStar):
        if self.settings.spectral:
            self.settings.apply_color(pstar.star.spectral_class, self._painter)
            # находим нужные координаты и по ним рисуем
            x, y = pstar.cx - pstar.diameter // 2, pstar.cy - pstar.diameter // 2
            self._painter.drawEllipse(int(x), int(y), int(pstar.diameter), int(pstar.diameter))

    # def _draw_object(self, pos: Horizontal, star: Star):
    #     if not star is None:
    #         if self.settings.spectral:
    #             self.settings.apply_color(star.spectral_class, self._painter)
    #         diameter = self._get_size(star.magnitude)
    #     else:
    #         self.settings.apply_color('up', self._painter)
    #         diameter = self._get_size(-1)
    #     # находим угол между направлением взгляда камеры и направлением на звезду
    #     # если угол <= радиусу обзора, то звезда отображается на экране
    #     if self.watcher.see.angle_to(pos) <= self.watcher.radius:
    #         # вычисляем изменение координаты звезды относительно направления камеры и проецируем на плоскость экрана
    #         delta = pos.to_point() - self.watcher.see.to_point()
    #         prj_delta = delta.rmul_to_matrix(self.watcher.transformation_matrix)
    #         # используем функцию distortion которая на основе координат в трехмерном пространстве и радиуса обзора
    #         # камеры вычисляет искажение изображения, а именно смещение координат и уменьшение диаметра звезды
    #         dx, dy = self._distortion(prj_delta.x, prj_delta.y, self.watcher.radius, prj_delta.z)
    #         diameter, _ = self._distortion(diameter, 0, self.watcher.radius, prj_delta.z)
    #         # вычисляются координаты отрисовки эллипса на плоскости экрана
    #         cx, cy = self._width // 2 + dx, self._height // 2 + dy
    #         x, y = cx - diameter // 2, cy - diameter // 2
    #         self._painter.drawEllipse(int(x), int(y), int(diameter), int(diameter))

    def _draw_background(self):
        self.settings.apply_color("sky", self._painter)  # устанавливаем цвет
        self._painter.drawRect(0, 0, self.width,
                               self.height)  # рисуем прямоугольник с координатами (0, 0) с данной высотой и шириной

    # def _draw_up(self):
    #     self._draw_object(Horizontal(0, 90), None)
    #     self._draw_object(Horizontal(0, 90), None)

    def _draw_see(self):
        self.settings.apply_color('see', self._painter)  # устанавливаем цвет
        diameter = self._get_size(-2)
        diameter, _ = self._distortion(diameter, 0, self.watcher.radius, 0)  # считаем диаметр на основании
        # параметров объекта
        # cx, cy = self._width // 2, self._height // 2  # определяем координаты центра
        # x, y = cx - diameter // 2, cy - diameter // 2  # по координатам центра и диаметру находим коорд левого
        # верхнего угла, далее рисуем круг
        x, y = self.centre[0] - diameter // 2, self.centre[
            1] - diameter // 2  # по координатам центра и диаметру находим коорд левого
        # верхнего угла, далее рисуем круг
        self._painter.drawEllipse(int(x), int(y), int(diameter), int(diameter))
