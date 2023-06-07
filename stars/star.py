from geometry.avector import Equatorial


class Star:

    def __init__(self, pos: Equatorial, constellation): #инициализируем звезду как ее коорд в экв. сист. и название созвездия
        self.position = pos
        self.constellation = constellation

    def __str__(self):
        return "\{{} in constellation {}\}".format(self.position, self.constellation)

    def __eq__(self, other):
        return self.position == other.position and self.constellation == other.constellation
