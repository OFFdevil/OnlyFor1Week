class Range:
    def __init__(self, minimum, maximum):
        self._minimum = minimum
        self._maximum = maximum

    @property
    def min(self):
        return self._minimum

    @property
    def max(self):
        return self._maximum

    @min.setter
    def min(self):
        return self._minimum

    @max.setter
    def max(self):
        return self._maximum

    @property
    def auto_min(self):
        return min(self.min, self.max)

    @property
    def auto_max(self):
        return max(self.min, self.max)

    @auto_min.setter
    def auto_min(self, value):
        self._minimum = value

    @auto_max.setter
    def auto_max(self, value):
        self._maximum = value

    def is_include(self, num):
        return self.min <= num <= self.max

    def __str__(self):
        return "[{}; {}]".format(self.min, self.max)


class Filter:
    def __init__(self, constellations: set, magnitude: Range):
        self.constellations = constellations
        self.magnitude = magnitude
