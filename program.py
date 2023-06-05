"""Графическая версия игры «Небо»"""
import datetime
import sys
from collections import namedtuple

from PyQt5 import QtWidgets

from geometry.equatorial import SecondEquatorial
from graphics.qgraphics import StarsWindow
from graphics.renderer.camera import Camera
from stars.parser import TxtDataBaseParser
from stars.skybase import SkySphere


def run(observer: Camera, sky_sphere: SkySphere, start_time: datetime.datetime):
    """Запуск логики «Неба»"""
    app = QtWidgets.QApplication([])

    wnd = StarsWindow(observer, sky_sphere, start_time)
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
        start_time = datetime.datetime.strptime(args.datetime, "%d-%m-%Y %H:%M:%S")
    except Exception:
        start_time = datetime.datetime.now()
    # TODO
    sight_vector = SecondEquatorial(args.vector[0], args.vector[1])
    observer = Camera(args.position[0], args.position[1], args.radius, sight_vector)
    star_parser = TxtDataBaseParser()
    stars = star_parser.parse_dir(args.catalog)
    sky_sphere = SkySphere(stars)
    sys.exit(run(observer, sky_sphere, start_time))


if __name__ == '__main__':
    main()
