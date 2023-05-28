from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtGui import QColor
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import QApplication

from graphics.camera import Camera
from graphics.sphere import Sphere
from vectors.vector import Vector


class Renderer(QGLWidget):
    # создаем конструктор, наследуем от QWidget
    def __init__(self):
        super().__init__()  # доступ к унаследованным методам от QWidget
        # которые переопределены в классе
        self.setGeometry(300, 300, 300, 220)  # задаем размеры окна
        self.setWindowTitle('Renderer')  # заголовок
        self.show()
        self._objects = []  # создали массив, с котором дальше будем работать
        self.bckg_color = QColor(0, 0, 0)
        self.camera = Camera()

    def initializeGL(self):
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glLoadIdentity()
        self.camera = Camera()
        # gluPerspective(*self.camera.perspective_params)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glLoadIdentity()

        # glLoadIdentity()
        # gluPerspective(*self.camera.perspective_params)
        gluPerspective(*self.camera.perspective_params)
        gluLookAt(*self.camera.look_params)
        # glFrustum(-50, 50, -50, 50, 0.1, 100)

        # gluSphere(GLU.gluNewQuadric(), 1, 100, 100)
        for sphere in self.objects:
            glColor(*sphere.color)
            glTranslated(sphere.centre.x, sphere.centre.y, sphere.centre.z)
            gluSphere(gluNewQuadric(), sphere.radius, 1000, 1000)
            glTranslated(-sphere.centre.x, -sphere.centre.y, -sphere.centre.z)
        glPopMatrix()
        glFlush()

    @property  # создали геттер для objects
    def objects(self):
        return self._objects

    @objects.setter  # создали сеттер от objects (название должно быть одинаковым)
    def objects(self, value):
        self._objects = []
        for i in value:  # перебор всех значений массива
            if not isinstance(i, Sphere):
                raise TypeError("Can not render '" + str(i) + "'")
            self._objects.append(i)  # добавление элементов, если не выдана ошибка
        self.repaint()


if __name__ == '__main__':
    app = QApplication(['Yo'])
    window = Renderer()
    s = Sphere(1)
    s.centre = Vector(0.5, 0, 0)
    window.objects.append(s)
    window.show()
    app.exec_()
