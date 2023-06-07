"""Графическая версия игры «Небо»"""
import datetime
import sys
from collections import namedtuple

from PyQt5 import QtWidgets

from geometry.avector import Equatorial, Horizontal
from graphics.qgraphics import StarsWindow
from graphics.renderer.camera import Camera
from graphics.renderer.watcher import Watcher
from stars.parser import TxtDataBaseParser
from stars.skybase import SkyBase


#TODO: create sky_logic.pu
#TODO: upgrade ui
#TODO: create see to contellar

def run(watcher: Watcher, sky_sphere: SkyBase):
    """Запуск логики «Неба»"""
    app = QtWidgets.QApplication([])

    wnd = StarsWindow(watcher, sky_sphere)
    center = app.desktop().availableGeometry().center()
    wnd.move(center.x() - wnd.width() // 2, center.y() - wnd.height() // 2)
    wnd.show()

    return app.exec_()


def main():
    """Точка входа в приложение"""
    #           LONGITUDE LATITUDE,       ...      AZIMUTH ALTITUDE , ..., ..., ..., ...
    Args = namedtuple("Args", ["position", "radius", "vector", "datetime", "catalog"])
    args = Args((60.6125, 56.8575), 60, (0, 89), None, r'C:\Users\..\Github\pysky\stars\stars\txt')
    # TODO

    try:
        start_time = datetime.datetime.strptime(args.datetime, "%d-%mass-%Y %H:%M:%S")
    except Exception:
        start_time = datetime.datetime.now()
    # TODO
    sight_vector = Horizontal(args.vector[0], args.vector[1])
    camera = Camera(args.radius, sight_vector)
    watcher = Watcher(Horizontal(args.position[0], args.position[1]), start_time, camera)
    star_parser = TxtDataBaseParser()
    stars = star_parser.parse_dir(args.catalog)
    sky_sphere = SkyBase(stars)
    sys.exit(run(watcher, sky_sphere))


if __name__ == '__main__':
    main()
