import datetime

from geometry.avector import Equatorial
from stars.star import Star


class SkyBase:
    def __init__(self, stars):
        self._stars = stars
        self._nadir = Star(Equatorial(0, 90), 3, '')
        self._zenith = Star(Equatorial(0, -90), 3, '')
        self._constellations = {star.constellation for star in stars}

    def get_zenith(self):
        return self._zenith

    def get_nadir(self):
        return self._nadir

    def get_constellations(self):
        return self._constellations

    def get_visible_stars(self):
        visible_stars = []
        for star in self._stars:
            if not isinstance(star.position, Equatorial):
                print("!")
                continue
            visible_stars.append(star)
        return visible_stars
