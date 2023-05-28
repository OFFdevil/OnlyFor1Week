from vectors.vector import Vector


DIRECTIONS = {
    'up': Vector(0, 0, 1),
    'down': Vector(0, 0, -1),
    'left': Vector(0, -1, 0),
    'right': Vector(0, 1, 0),
    'forward': Vector(1, 0, 0),
    'backward': Vector(-1, 0, 0)
}


def string_to_direction(s):
    if not s in DIRECTIONS:
        return None
    return DIRECTIONS[s]
