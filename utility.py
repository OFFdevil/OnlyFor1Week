import datetime
from PyQt5.QtGui import QColor


def profile(foo):
    def decorated(*args, **kwargs):
        prev = foo.__last_call_time if "__last_call_time" in dir(foo) else None
        lct = foo.__last_call_time = datetime.datetime.now()
        kwargs["exec_delta"] = (lct - prev) if not prev is None else None
        return foo(*args, **kwargs)

    return decorated


def hexstr_to_color(s: str):
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:], 16)
    return QColor(r, g, b)


def try_or_print(foo):
    def decorated(*args, **kwargs):
        try:
            return foo(*args, **kwargs)
        except Exception as e:
            print("Exception in {}({}; {}): {}".format(foo.__name__, e, args, kwargs))
            return None

    return decorated


def foreach(name, enum):
    def decorator(foo):
        def decorated(*args, **kwargs):
            if not kwargs:
                kwargs = {}
            results = []
            for i in enum:
                kwargs[name] = i
                results.append(foo(*args, **kwargs))
            return results

        return decorated

    return decorator
