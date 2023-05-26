import sys
from PyQt5.QtWidgets import QApplication
from graphics.renderer import Renderer
from vectors.vector import Vector

for a in range(-180, 180):
    for h in range(-90, 90):
        v = Vector.from_horizontal(h, a, 5)
        hor = v.to_horizontal()
        d = (Vector(a, h, 0) - Vector(hor.a, hor.h, 0)).length
        if d > 0.1:
            print(d)

sys.exit(0)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Renderer()
    ex.objects = [1, 2, 3]
    sys.exit(app.exec_())
