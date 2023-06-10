import datetime
from stars.sky_math import StarTimeHelper

'''https://en.wikipedia.org/wiki/Sidereal_time'''


class StarTime:
    @staticmethod
    def from_local(longitude: float, local: datetime):
        return StarTime(StarTimeHelper.get_star_hour(longitude, local))

    def __init__(self, hours: int):
        self._hours = hours

    @property
    def total_hours(self):
        return self._hours

    @property
    def total_minutes(self):
        return self.total_hours * 60

    @property
    def total_seconds(self):
        return self.total_minutes * 60

    @property
    def total_degree(self):
        return self.total_hours * 15

    def __int__(self):
        return int(self.total_seconds)

    def __float__(self):
        return float(self.total_seconds)

    def __str__(self):
        return str(int(self))
