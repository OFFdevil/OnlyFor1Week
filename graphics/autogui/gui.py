from graphics.autogui.item import Item
from graphics.autogui.label import Label


class GUI(Item):
    def __init__(self, name: str):
        super().__init__()
        self._nested = []  # храним инфу про вложенные виджеты и контейнеры
        self.addLayout(Label(name, True), 0, 0)  # метод для добавления
        # нового компонента в текущую сетку
        self.setContentsMargins(10, 1, 1, 10)  # устанавливает величины
        # полей содержимого виджета

    def add(self, item: Item) -> Item:  # добавляет новый компонент item
        # к текущему виджету на позицию
        self._nested.append(item)
        self.addLayout(item, len(self._nested) + 1, 0)
        return item  # возвращает добавленный элемент

    def try_load(self):
        pass

    def try_save(self):
        for h in self._nested:
            if not h.try_save():
                h.try_load()

    def handle(self):  # сохраняет и загружает обновленное
        # состояние всех элементов текущего контейнера
        self.try_save()  # сохранили текущее состояние всех вложенных элементов
        # текущего контейнера
        self.try_load()  # метод, чтобы загрузить обновленное состояние вложенных элементов
        # из предыдущего сохранения


#example:
#layout = GUI()
#layout.add()