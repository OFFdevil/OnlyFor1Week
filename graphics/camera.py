from vectors.vector import Vector


class Camera:
    def __init__(self):
        self.position = Vector(0, 0, 0)  # вектор, указывающий на
        # позицию камеры в 3д пространстве
        self.view = Vector(1, 0, 0)  # указывает, куда смотрит камера
        self.up = Vector(0, 0, 1)  # указывает на вертикальную ось камеры
        self.angle = 60  # угол обзора камеры = поле зрения

    @property  # превратили метод в getter
    # property пишем перед getter-ом
    def look_params(self):  # возвращает кортеж параметров, которые
        # могут быть использованы для настройки OpenGL камеры
        eye = self.position  # позиция глаза
        centre = self.position + self.view  # точка, на которую смотрит камера
        up = self.up  # вертикальная ось камеры
        return eye.x, eye.y, eye.z, centre.x, centre.y, centre.z, up.x, up.y, up.z

    @property
    def perspective_params(self):  # параметры: угол обзора,
        # соотношение сторон, ближняя и дальняя плоскость отсечения
        return self.angle, 1.33, 0.1, 100.0
