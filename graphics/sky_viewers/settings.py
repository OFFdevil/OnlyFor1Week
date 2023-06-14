from math import log10
from geometry.sky_math import sign


class ControllableSkySettings:
    def __init__(self):
        self.second_per_second = 1
        self.zoom = 1

    @property
    def speed_rank(self):
        if self.second_per_second == 0:
            return 0
        return (log10(abs(self.second_per_second)) + 1) * sign(self.second_per_second)

    @speed_rank.setter
    def speed_rank(self, value):
        if value > 10:
            raise ValueError()
        self.second_per_second = 10 ** (abs(value) - 1) * sign(value)
