from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter
from geometry.horizontal import Horizontal
from geometry.equatorial import Equatorial
from graphics.renderer.settings import RenderSettings
from graphics.renderer.watcher import Watcher
from stars.star import Star


# функция считает искажение, которое возникает при съёмке с широкоугольной камеры (искажение рыбьего глаза) она
# вычисляет координаты точки на изображении с помощью формулы с использованием: dx, dy- координаты точки на плоском
# изображении, sight_radius - радиус обзора широкоугольной камеры, z - расстояние между плоскостью
# изображения и центром камеры
def fisheye_distortion(x, y, radius, z):
    r = radius * 10 / (1 - abs(z)) ** 2
    return x * r, y * r


# функция осуществляет шкалирование координат x, y на основе радиуса обзора
def scale_distortion(x, y, radius, z):
    return x * radius * 10, y * radius * 10


# создали класс Canvas, наследующийся от QWidget
# в целом класс отвечает за прорисовку неба и звезд, содержит в себе несколько методов для рисования звезд на виджете
class Renderer:
    def __init__(self, watcher: Watcher):
        super().__init__()
        self._buffer = QImage(QSize(0, 0), QImage.Format_RGB32)  # создаем объект размером 0*0
        self._painter = QPainter()
        self.settings = RenderSettings()
        self.watcher = watcher

        # ширина и высота изображения, заданного для отрисовки
        self._width = 0
        self._height = 0
        self._distortion = fisheye_distortion  # хранит значение искажения в съемке с широкоугольной камеры

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
            self._buffer = QImage(QSize(self.width, self.height), QImage.Format_RGB32)

    @height.setter  # сеттер высоты, аналогично для нее
    def height(self, value):
        if value != self.height:
            self._height = value
            self._buffer = QImage(QSize(self.width, self.height), QImage.Format_RGB32)

    # используем значение параметра fisheye, по нему определяем нужно ли имитировать эффект съёмки широкоугольной
    # камеры или нет
    def render(self, stars: list) -> QImage:
        self._distortion = fisheye_distortion if self.settings.fisheye else scale_distortion

        self._painter.begin(self._buffer)
        self._draw_background()  # рисуем фон
        self.settings.apply_color("star", self._painter)  # задаем цвет звезд
        for o in (self._apply_time_rotation(s) for s in stars):
            self._draw_object(o)  # прорисовываем каждую звезду
        self.settings.apply_color("up", self._painter)
        self._draw_object(Horizontal(0, 90))
        self.settings.apply_color("down", self._painter)
        self._draw_object(Horizontal(0, -90))
        self._painter.end()
        return self._buffer

    def _apply_time_rotation(self, star: Star):
        return star.position.to_horizontal_system(self.watcher.star_time.total_degree % 360, self.watcher.position.h)

    def _draw_object(self, pos: Horizontal):
        diameter = 0.005  # значение по умолчанию
        # находим угол между направлением взгляда камеры и направлением на звезду
        # если угол <= радиусу обзора, то звезда отображается на экране
        if self.watcher.see.angle_to(pos) <= self.watcher.radius:
            # вычисляем изменение координаты звезды относительно направления камеры и проецируем на плоскость экрана
            delta = pos.to_point() - self.watcher.see.to_point()
            prj_delta = delta.rmul_to_matrix(self.watcher.transformation_matrix)
            # используем функцию distortion которая на основе координат в трехмерном пространстве и радиуса обзора
            # камеры вычисляет искажение изображения, а именно смещение координат и уменьшение диаметра звезды
            dx, dy = self._distortion(prj_delta.x, prj_delta.y, self.watcher.radius, prj_delta.z)
            diameter, _ = self._distortion(diameter, 0, self.watcher.radius, prj_delta.z)
            # вычисляются координаты отрисовки эллипса на плоскости экрана
            cx, cy = self._width // 2 + dx, self._height // 2 + dy
            x, y = cx - diameter // 2, cy - diameter // 2
            self._painter.drawEllipse(int(x), int(y), int(diameter), int(diameter))

    def _draw_background(self):
        self.settings.apply_color("sky", self._painter)  # использует свет фона sky
        self._painter.drawRect(0, 0, self.width,
                               self.height)  # рисуем прямоугольник с координатами (0, 0) с данной высотой и шириной
