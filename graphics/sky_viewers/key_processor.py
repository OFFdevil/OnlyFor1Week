class KeyProcessorFAPIIData:
    def __init__(self, processor, name: str, key):
        self._processor = processor
        self._name = name
        self._key = key

    def with_arguments(self, *args, **kwargs):
        self._processor.bind(self._key, self._name, (args, kwargs))
        return KeyProcessorFAPIIKey(self._processor, self._name)


class KeyProcessorFAPIIKey:
    def __init__(self, processor, name: str):
        self._processor = processor
        self._name = name

    def when_pressed(self, key) -> KeyProcessorFAPIIData:
        self._processor.bind(key, self._name)
        return KeyProcessorFAPIIData(self._processor, self._name, key)


class KeyProcessor:
    def __init__(self):
        self._instructions = {}
        self._keys = {}

    def should_be_called(self, name_or_instruction, instruction=None) -> KeyProcessorFAPIIKey:
        name = name_or_instruction if instruction is not None else str(name_or_instruction)
        instruction = instruction if instruction is not None else name_or_instruction
        self._instructions[name] = instruction
        return KeyProcessorFAPIIKey(self, name)

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
            data = (tuple(), dict())
        instruction(*data[0], **data[1])
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
