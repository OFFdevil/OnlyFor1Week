from PyQt5 import Qt

from PyQt5.QtWidgets import QApplication
from graphics.renderer import Renderer
from graphics.sphere import Sphere
from graphics.utility import string_to_direction
from vectors.vector import Vector, Horizontal


class ControllableRenderer(Renderer):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controllable renderer")
        self.keymap = {32: 'up', 90: 'down', 87: 'forward', 65: 'left', 83: 'backward', 68: 'right', 16777235: 'eup',
                       16777234: 'eleft', 16777237: 'edown', 16777236: 'eright'}
        self.move_step = 0.5
        self.turn_step = 10

    def _move(self, action):
        d = string_to_direction(action)
        if d is None:
            return False
        self.camera.position += d * self.move_step

    def _turn(self, action):
        vi = self.camera.view.to_horizontal()
        up = self.camera.up.to_horizontal()
        if action == 'eup':
            try:
                self.camera.view = Vector.from_horizontal(*Horizontal(vi.h + self.turn_step, vi.a, 1))
                self.camera.up = Vector.from_horizontal(*Horizontal(up.h + self.turn_step, up.a, 1))
            except Exception as e:
                print(e)

    def keyPressEvent(self, e):
        code = e.key()
        if code in self.keymap:
            action = self.keymap[code]
            if not self._move(action):
                self._turn(action)
            self.repaint()
        else:
            print(code)


if __name__ == '__main__':
    app = QApplication(['Yo'])
    window = ControllableRenderer()
    s = Sphere(1)
    s.centre = Vector(0.5, 0, 0)
    window.objects.append(s)
    window.show()
    app.exec_()
