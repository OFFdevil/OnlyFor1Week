import datetime

from geometry.equatorial import SecondEquatorial
from stars.star import Star


class SkySphere:
    def __init__(self, stars):
        self._stars = stars
        self._nadir = Star(SecondEquatorial(0, 90), 3, '')
        self._zenith = Star(SecondEquatorial(0, -90), 3, '')
        self._constellations = {star.constellation for star in stars}

    def get_zenith(self):
        return self._zenith

    def get_nadir(self):
        return self._nadir

    def get_constellations(self):
        return self._constellations

    def get_visible_stars(self, observer, date_time: datetime.datetime):
        visible_stars = []
        for star in self._stars:
            if not isinstance(star.position, SecondEquatorial):
                print("!")
                continue
            visible_stars.append(star)
        return visible_stars
