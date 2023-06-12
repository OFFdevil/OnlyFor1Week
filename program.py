import os
from os.path import join
from argparse import ArgumentParser
import datetime
from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import QSound
from graphics.renderer.renderer import Renderer
from graphics.renderer.settings import Settings
from stars.filter import Filter, Range
from stars.skydatabase import SkyDataBase
from geometry.horizontal import Horizontal
from task import create_task, Task
from graphics.sky_viewers.key_controllable_sky import KeyControllableSky
from graphics.sky_viewers.sky import Sky
from graphics.renderer.camera import Camera
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.mouse_controllable_sky import MouseControllableSky
from graphics.sky_viewers.named_sky import NamedSky
from stars.parser import TxtDataBaseParser
import sys


def gui_mode(task: Task):
    app = QtWidgets.QApplication([])
    sky = NamedSky(task.watcher, task.database, task.filter)
    sky.renderer.settings = task.render_settings
    sky.viewer.out_file_name = task.out_file_name
    sky.animation = task.animation
    if task.pause:
        sky.switch_pause()
    if task.full_screen_mode:
        sky.switch_full_screen()


def console_mode(task: Task):
    renderer = Renderer(task.watcher)
    renderer.settings = task.render_settings
    image = renderer.render(task.database.get_stars(task.filter), False)
    fname = task.watcher.local_time.strftime(task.out_file_name)


if __name__ == "__main__":
    task = create_task()
    if task.console_mode:
        console_mode(task)
    else:
        gui_mode(task)
