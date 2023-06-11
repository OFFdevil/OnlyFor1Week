import datetime
import os
from PyQt5 import QtWidgets
from geometry.horizontal import Horizontal
from graphics.sky_viewers.key_controllable_sky import KeyControllableSky
from graphics.sky_viewers.sky import Sky
from graphics.renderer.camera import Camera
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.mouse_controllable_sky import MouseControllableSky
from graphics.sky_viewers.named_sky import NamedSky
from stars.parser import TxtDataBaseParser


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


class City(Horizontal):
    def __init__(self, широта, долгота):
        super().__init__(долгота, широта)


MAGNITOGORSK = City(53, 59)
YEKATERINBURG = City(56, 60)


def main():
    sky_base = TxtDataBaseParser().parse(
        get_all_lines_in_dir(r'stars/stars', '.txt'))
    camera = Camera(Horizontal(0, 90), 60)
    watcher = Watcher(MAGNITOGORSK, datetime.datetime.now(), camera)

    app = QtWidgets.QApplication([])
    NamedSky(watcher, sky_base)
    app.exec()


if __name__ == '__main__':
    main()
