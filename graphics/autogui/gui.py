from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget

from graphics.autogui.cast_tools import to_widget

from graphics.autogui.item import Item
from graphics.autogui.label_item import LabelItem


class GUI(Item):
    def __init__(self, name: str):
        super().__init__(False)
        self._nested = []  # храним инфу про вложенные виджеты и контейнеры
        self.setTitle(name)

    def add(self, item: Item) -> Item:  # добавляет новый компонент item
        # к текущему виджету на позицию
        self._nested.append(item)
        self.layout.addWidget(item, len(self._nested), 0)
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
