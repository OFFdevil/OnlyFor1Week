from geometry.equatorial import Equatorial


class Star:

    def __init__(self, pos: Equatorial,
                 constellation):  # инициализируем звезду как ее коорд в экв. сист. и название созвездия
        self._position = pos
        self._constellation = constellation

    @property
    def position(self):
        return self._position

    @property
    def constellation(self):
        return self._constellation

    def __str__(self):
        return "{{at in constellation {}}}".format(self.position, self.constellation)

    def __eq__(self, other):
        return self.position == other.position and self.constellation == other.constellation
