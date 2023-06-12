import os
from argparse import ArgumentParser
import sys
import datetime
from collections import namedtuple
from os.path import join
from geometry.horizontal import Horizontal
from graphics.renderer.camera import Camera
from graphics.renderer.settings import Settings
from graphics.renderer.watcher import Watcher
from stars.filter import Filter
from stars.filter import Range
from stars.parser import TxtDataBaseParser

BUILTIN_CITIES = {"MGN": Horizontal(59, 53), "EKB": Horizontal(60, 56)}

parser = ArgumentParser(
    description="Space simulator",
    epilog=""
)

# различные аргументы командной строки
parser.add_argument('-c', '--console', action='store_true', help="don`t use gui for visualization")
parser.add_argument('-m', '--music', action='store_true', help="enable music")
parser.add_argument('-b', '--base', type=str, metavar='PATH', default=join('stars', 'stars', 'txt'),
                    help="path to star date base")
parser.add_argument('-o', '--out', type=str, metavar='PATH', default='stars when %d.%m.%Y %H_%M_%S.jpg',
                    help="name of resulted image (you can use datetime mask)")
parser.add_argument('-f', '--full-screen', action='store_true', help="maximize window")
parser.add_argument('--on-pause', action='store_true', help="startup on pause")
parser.add_argument('--disable-animation', action='store_true', help="disable startup animation")

parser.add_argument('-d', type=str, metavar='DATETIME', default=None, help="datetime for rendering (use d.m.Y H:M:S)")
parser.add_argument('-p', type=float, nargs=2, metavar=('LONG', 'LAT'), default=(53, 59), help="position of watcher")
parser.add_argument('-s', type=float, nargs=2, metavar=('A', 'H'), default=(59, 53),
                    help="see direction (in horizontal)")

parser.add_argument('--see-up', action='store_true', help="see always up")
parser.add_argument('--city', choices=BUILTIN_CITIES.keys(), default=None, help="builtins cities")

parser.add_argument('--fisheye', type=bool, metavar="", default=True, help="enable fisheye distortion?")
parser.add_argument('--spectral', type=bool, metavar="", default=True, help="enable spectral depended star color?")
parser.add_argument('--magnitude', type=bool, metavar="", default=True,
                    help="enable magnitude depended star size transformation?")
parser.add_argument('--disable-effects', action='store_true', help="disable all visual effects")

parser.add_argument('--see-points', type=bool, metavar="", default=True, help="show see critical points(0, +-90)?")
parser.add_argument('--centre-direction', type=bool, metavar="", default=True, help="show centre direction?")
parser.add_argument('--compass', type=bool, metavar="", default=True, help="show compass?")
parser.add_argument('--disable-points', action='store_true', help="disable all points")

parser.add_argument('--magnitude-range', type=float, nargs=2, metavar=('MIN', 'MAX'), default=(-1, 10),
                    help='Magnitude filter for stars')
parser.add_argument('--constellations', type=str, nargs='*', metavar='NAME', default=None,
                    help='Constellations filter for stars')


# принимает строку в формате даты и времени и возвращает нужный формат объекта
def extract_time(string):
    full_year = ["%d.%m.%Y %H:%M:%S", "%d.%m.%Y %H:%M", "%d.%m.%Y %H", "%d.%m.%Y"]
    short_year = ["%d.%m.%y %H:%M:%S", "%d.%m.%y %H:%M", "%d.%m.%y %H", "%d.%m.%y"]
    time = ["%H:%M:%S", "%H:%M", "%H"]
    for f in full_year + short_year + time:
        try:
            dt = datetime.datetime.strptime(string, f)
            if f in time:
                n = datetime.datetime.now()
                dt = datetime.datetime(n.year, n.month, n.day, dt.hour, dt.minute, dt.second)
            return dt
        except:
            pass
    return full_year, short_year, time


# получаем все файлы из нужной папки
def get_all_files_in_dir(path: str, ext: str):
    for fn in os.listdir(path):
        if fn.endswith(ext):
            yield os.path.join(path, fn), fn.split('.')[0]


def get_all_lines_in_dir(path: str, ext: str):
    for p, fn in get_all_files_in_dir(path, ext):
        with open(p, 'r') as file:
            for line in file:
                yield line, fn


Task = namedtuple('Task',
                  ['database', 'filter', 'watcher', 'render_settings', 'out_file_name', 'music_mode', 'console_mode',
                   'full_screen_mode', 'pause', 'animation'])


def create_task():  # анализируем парамтеры командной строки, задает базу данных и др параметры
    # возвращаем объект, содержащий информацию о базе данных
    args = parser.parse_args()
    dt = extract_time(args.d)
    if isinstance(dt, tuple):
        if args.d is not None:
            print('Bad datetime, use:\n\t{}\n\t{}\n\t{}'.format(*(str.join(', ', i) for i in dt)))
            sys.exit(1)
        else:
            dt = datetime.datetime.now()
    database = TxtDataBaseParser().parse(get_all_lines_in_dir(args.base, '.txt'))

    r = rset = Settings()
    if not args.disable_effects:
        r.fisheye, r.spectral, r.magnitude, = args.fisheye, args.spectral, args.magnitude
    else:
        r.fisheye, r.spectral, r.magnitude = False, False, False

    if not args.disable_points:
        r.see_points, r.screen_centre, r.compass = args.see_points, args.centre_direction, args.compass
    else:
        r.see_points, r.screen_centre, r.compass = False, False, False

    pos = BUILTIN_CITIES[args.city] if args.city else Horizontal(args.p[1], args.p[0])
    see = pos if args.see_up else Horizontal(*args.s)
    camera = Camera(see, 60)
    watcher = Watcher(pos, dt, camera)

    consts = args.constellations if args.constellations else database.constellations
    m_range = Range(min(*args.magnitude_range), max(*args.magnitude_range))
    selector = Filter(consts, m_range)

    return Task(database, selector, watcher, rset, args.out, args.music, args.console, args.full_screen, args.on_pause,
                not args.disable_animation)
