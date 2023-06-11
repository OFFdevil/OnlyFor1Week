class Range:  # класс, отвечающий за текущий промежуток значений размеров звезды
    def __init__(self, minimum, maximum):
        self._minimum = minimum
        self._maximum = maximum

    @property
    def min(self):
        return self._minimum

    @property
    def max(self):
        return self._maximum

    def is_include(self, num):
        return self.min <= num <= self.max

    def __str__(self):
        return "[{}; {}]".format(self.min, self.max)


class Filter:
    def __init__(self, constellations: set, magnitude: Range):
        self.constellations = constellations
        self.magnitude = magnitude
