from task import create_task, Task

from PyQt5 import QtWidgets
from graphics.renderer.renderer import Renderer
from graphics.sky_viewers.named_sky import NamedSky


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
    else:
        app.exec()


def console_mode(task: Task):
    renderer = Renderer(task.watcher)
    renderer.settings = task.render_settings
    image = renderer.render(task.database.get_stars(task.filter), False)
    fname = task.watcher.local_time.strftime(task.out_file_name)
    image.save(fname)
    print("Image has been successful saved to {}".format(fname))


if __name__ == "__main__":
    task = create_task()
    if task.console_mode:
        console_mode(task)
    else:
        gui_mode(task)
