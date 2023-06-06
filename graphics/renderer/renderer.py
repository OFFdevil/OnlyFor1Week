import math
import datetime
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget
from geometry.avector import Horizontal, Equatorial
from graphics.renderer.camera import Camera
from graphics.renderer.settings import RenderSettings
from stars.skybase import SkyBase
from stars.star import Star


# функция считает искажение, которое возникает при съёмке с широкоугольной камеры (искажение рыбьего глаза) она
# вычисляет координаты точки на изображении с помощью формулы с использованием: dx, dy- координаты точки на плоском
# изображении, sight_radius - радиус обзора широкоугольной камеры, z - расстояние между плоскостью
# изображения и центром камеры
def fisheye_distortion(dx, dy, sight_radius, z):
    r = sight_radius * 10 / (1 - abs(z))
    return dx * r, dy * r


# создали класс Canvas, наследующийся от QWidget
# в целом класс отвечает за прорисовку неба и звезд, содержит в себе несколько методов для рисования звезд на виджете
class Canvas(QWidget):
    def __init__(self, camera: Camera, dt: datetime):
        super().__init__()
        self._buffer = QImage(self.size(), QImage.Format_RGB32)
        self._painter = QPainter()
        # используем настройки и камеру из других файлов
        self.settings = RenderSettings()
        self.camera = camera
        self.datetime = dt

        self._width = 0
        self._height = 0
        self.objects = []

    def repaint(self):
        self._width, self._height = self.width(), self.height()  # определяем высоту, ширину
        self._painter.begin(self._buffer)
        self._draw_background(self._painter)  # закрашивание холста
        self.settings.apply_color("star", self._painter)  # установка цвета
        for o in self.objects:  # отображение всех объектов на холсте
            self._draw_objects(o, self._painter)
        self.settings.apply_color("point", self._painter)
        # прорисовка звезд на северном и южном полушариях
        self._draw_objects(Star(Equatorial(0, 90), 3, ''), self._painter, False)
        self._draw_objects(Star(Equatorial(0, -90), 3, ''), self._painter, False)
        self._painter.end()  # закончили покраску
        super().repaint()  # добавление изменений на холст перед отображением

    # функция вычисляет положение звезды на небосводе в данный момент, далее метод либо переводит координаты звезды в
    # горизонтальную систему, либо использует уже подготовленные
    def _draw_objects(self, star: Star, p, translate=True):
        pos = star.position.to_horizontal_system(
            self.camera.latitude,
            self.camera.get_lst(self.datetime) * 15  # TODO: WTF???
        )
        if not translate:
            pos = Horizontal(star.position.alpha, star.position.delta)

            diameter = 2
            delta = pos.to_point() - self.camera.sight_vector.to_point()
            prj_delta = delta.rmul_to_matrix(self.camera.transformation_matrix)
            r = self.camera.sight_vector.angle_to(pos)
            # В зависимости от положения звезды на небосводе и угла обзора камеры, метод отображает звезду на графике
            # с помощью эллипса определенного размера
            if r <= self.camera.sight_radius:
                dx, dy = fisheye_distortion(prj_delta.x, prj_delta.y, self.camera.sight_radius, prj_delta.z)
                cx, cy = self._width // 2 + dx, self._height // 2 + dy
                x, y = cx - diameter // 2, cy - diameter // 2
                p.drawEllipse(x, y, diameter, diameter)

    def _draw_background(self, p):
        self.settings.apply_color("sky", p)  # использует свет фона sky и принимает его к p
        p.drawRect(0, 0, self.width(),
                   self.height())  # рисуем прямоугольник с координатами (0, 0) с определенной высотой и шириной

    def resizeEvent(self, event):  # смена размера
        self._buffer = self._buffer.scaled(self.size())

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self._buffer)  # рисуем изображение начиная с точки (0, 0)
        painter.end()
