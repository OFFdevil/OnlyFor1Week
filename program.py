import datetime
import os
import sys
from collections import namedtuple
from PyQt5 import QtWidgets
from geometry.avector import Horizontal
from graphics.crenderer import StarsWindow
from graphics.renderer.camera import Camera
from graphics.renderer.watcher import Watcher
from stars.parser import TxtDataBaseParser
from stars.skydatabase import SkyDataBase


# TODO: create sky_logic.pu
# TODO: upgrade ui
# TODO: create see to contellar
# TODO: see (0, -90) at (56, -60) only северное полушарие!!! ВСЕ НОРМ
# TODO: see (0, 90) at (0, -90) only северное полушарие!!! ВСЕ НОРМ


def get_all_files_in_dir(path: str, ext: str):  # на вход принимает путь и расширение файла
    for fn in os.listdir(path):  # перебор всех файлов в директории
        if fn.endswith(ext):
            yield os.path.join(path, fn), fn.split('.')[0]
            # возвращает путь к файлу, если у него нужное расширение


def get_all_lines_in_dir(path: str, ext: str):
    for p, fn in get_all_files_in_dir(path, ext):
        # получили список файлов
        with open(p, 'r') as file:  # открываем каждый найденный файл
            for line in file:  # перебор строк в файле
                yield line, fn  # строка и имя файла без расширения возвращаются
                # в виде кортежа


def run(watcher: Watcher, sky_sphere: SkyDataBase):  # создает и запускает графический интерфейс
    """Запуск логики «Неба»"""
    app = QtWidgets.QApplication([])  # создали объект приложения

    wnd = StarsWindow(watcher, sky_sphere)  # сохранили в wnd
    center = app.desktop().availableGeometry().center()
    # вычислили центр рабочего экрана
    wnd.move(center.x() - wnd.width() // 2, center.y() - wnd.height() // 2)
    # переместили созданное окно в центр экрана
    wnd.show()  # отображает окно

    return app.exec_()


def main():
    """Точка входа в приложение"""
    #           LONGITUDE LATITUDE,       ...      AZIMUTH ALTITUDE , ..., ..., ..., ...
    Args = namedtuple("Args", ["position", "radius", "vector", "datetime", "catalog"])
    # создали именованный кортеж
    args = Args((60.6125, 56.8575), 60, (0, 89), None, r'C:\Users\..\Github\pysky\stars\stars\txt')
    # TODO

    try:
        start_time = datetime.datetime.strptime(args.datetime, "%d-%mass-%Y %H:%M:%S")
    except Exception:
        start_time = datetime.datetime.now()
    # TODO
    sight_vector = Horizontal(args.vector[0], args.vector[1])
    camera = Camera(args.radius, sight_vector)  # создали объект камера
    watcher = Watcher(Horizontal(args.position[0], args.position[1]), start_time, camera)
    star_parser = TxtDataBaseParser()
    sky_sphere = star_parser.parse(get_all_lines_in_dir(args.catalog, '.txt'))  # парсим
    sys.exit(run(watcher, sky_sphere))


if __name__ == '__main__':
    main()
