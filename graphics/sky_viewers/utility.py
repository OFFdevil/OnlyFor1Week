import datetime


def profile(foo): #профилирование функций. Декоратор для функций, у которых хотим узнать производительность/время работы
    def decorated(*args, **kwargs):
        prev = foo.__last_call_time if "__last_call_time" in dir(foo) else None
        lct = foo.__last_call_time = datetime.datetime.now()
        kwargs["exec_delta"] = (lct - prev) if prev is not None else None
        return foo(*args, **kwargs)

    return decorated


class KeyProcessor:
    def __init__(self):
        self._instructions = {}
        self._keys = {}

    def register(self, name, instruction):
        self._instructions[name] = instruction
        return self

    def bind(self, key, name, data=None):
        self._keys[key] = (name, data)
        return self

    def alias(self, key, *aliases):
        for alias in aliases:
            self._keys[alias] = self._keys[key]
        return self

    def execute(self, key):
        pair = self._find_key(key)
        if pair is None:
            return False
        name, data = pair[0], pair[1]
        if not name in self._instructions:
            return False
        instruction = self._instructions[name]
        if data is None:
            data = tuple()
        instruction(*data)
        return True

    def _find_key(self, key):
        if key in self._keys:
            return self._keys[key]
        if str(key) in self._keys:
            return self._keys[str(key)]
        if str(key).lower() in self._keys:
            return self._keys[str(key).lower()]
        if str(key).upper() in self._keys:
            return self._keys[str(key).upper()]
        return None
