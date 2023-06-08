from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter
from geometry.avector import Horizontal, Equatorial

from graphics.renderer.settings import RenderSettings
from graphics.renderer.watcher import Watcher
from stars.star import Star


# функция считает искажение, которое возникает при съёмке с широкоугольной камеры (искажение рыбьего глаза) она
# вычисляет координаты точки на изображении с помощью формулы с использованием: dx, dy- координаты точки на плоском
# изображении, sight_radius - радиус обзора широкоугольной камеры, z - расстояние между плоскостью
# изображения и центром камеры
def fisheye_distortion(x, y, sight_radius, z):
    r = sight_radius * 10 / (1 - abs(z)) ** 2
    return x * r, y * r


# функция осуществляет шкалирование координат x, y на основе радиуса обзора
def scale_distortion(x, y, sight_radius, z):
    return x * sight_radius * 10, y * sight_radius * 10


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
    def _load_distortion(self):
        self.distortion = fisheye_distortion if self.settings.fisheye else scale_distortion

    # функция выводит звездное небо в 3D, принимает на вход объект star, координаты которого будут нарисованы на экране
    # флаг translate указывает нужно ли переводить координаты звезды в горизонтальную систему координат
    def _draw_object(self, star: Star, p, translate=True):
        # выполняем перевод в горизонт систему координат, учитывая широту и текущее время
        pos = star.position.to_horizontal_system(self.watcher.position.delta, self.watcher.star_time.total_degree % 360)
        if not translate:  # если флаг не установлен, то используем оригинальную систему координат
            pos = Horizontal(star.position.alpha, star.position.delta)

        diameter = 0.01  # значение по умолчанию
        # вычисляем изменение координаты звезды относительно направления камеры и проецируем на плоскость экрана
        delta = pos.to_point() - self.watcher.sight_vector.to_point()
        prj_delta = delta.rmul_to_matrix(self.watcher.transformation_matrix)
        # находим угол между направлением взгляда камеры и направлением на звезду
        # если угол <= радиусу обзора, то звезда отображается на экране
        if self.watcher.sight_vector.angle_to(pos) <= self.watcher.eye_radius:
            # используем функцию distortion которая на основе координат в трехмерном пространстве и радиуса обзора
            # камеры вычисляет искажение изображения, а именно смещение координат и уменьшение диаметра звезды
            dx, dy = self._distortion(prj_delta.x, prj_delta.y, self.watcher.eye_radius, prj_delta.z)
            diameter, _ = self._distortion(diameter, 0, self.watcher.eye_radius, prj_delta.z)
            # вычисляются координаты отрисовки эллипса на плоскости экрана
            cx, cy = self._width // 2 + dx, self._height // 2 + dy
            x, y = cx - diameter // 2, cy - diameter // 2
            p.drawEllipse(x, y, diameter, diameter)

    def _draw_background(self, p):
        self.settings.apply_color("sky", p)  # использует свет фона sky и принимает его к p
        p.drawRect(0, 0, self.width,
                   self.height)  # рисуем прямоугольник с координатами (0, 0) с определенной высотой и шириной

    def render(self, stars: list) -> QImage:  # возвращает объект изображения
        self._load_distortion()

        self._painter.begin(self._buffer)
        self._draw_background(self._painter)  # рисуем фон
        self.settings.apply_color("star", self._painter)  # задаем цвет звезд
        for o in stars:
            self._draw_object(o, self._painter)  # прорисовываем каждую звезду
        self.settings.apply_color("up", self._painter)
        self._draw_object(Star(Equatorial(0, 90), ''), self._painter, False)
        self.settings.apply_color("down", self._painter)
        self._draw_object(Star(Equatorial(0, -90), ''), self._painter, False)
        self._painter.end()
        return self._buffer
