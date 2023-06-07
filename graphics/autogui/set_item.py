from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QPushButton

from graphics.autogui.item import Item


# создаем класс, который наследуется от Item
class CheckBoxSet(Item):
    def __init__(self, str_set, handler=None):
        super().__init__()
        self._src = set(str_set)  # в переменную сохраняем все множество значений, переданных в str_set
        self._selected = set()
        self._handlers = [] if handler is None else [handler]  # пустой список или передается обработчик, если handler
        # не был передан
        self._create_widget()  # методы создания виджетов и кнопок
        self._create_buttons()

    def _create_widget(self):
        self._model = QStandardItemModel()  # используем модель, которая будет хранить данные списка элементов
        for row in sorted(self._src):
            item = QStandardItem(row)  # для каждого элемента создаем экземпляр, который содержит текст элемента и
            # устанавливает флажок, начальное состояние
            item.setCheckState(False)
            item.setCheckable(True)
            item.setEditable(False)
            self._model.appendRow(item)

        # создаем виджет и устанавливаем обработчик щелчка на элементы списка
        view = QListView()
        view.setModel(self._model)
        view.clicked.connect(lambda: self._on_change())
        self._model.itemChanged.connect(lambda: self._on_change())

        self._lock = False
        self._widget = view
        self.addWidget(self._widget)

    def _create_buttons(self):
        # создаем кнопку none, обработчик событий по нажатию, который передает 0
        bclear = QPushButton("none")
        bclear.clicked.connect(lambda: self._change_state_for_all(0))
        self.addWidget(bclear)
        # создаем кнопку all, обработчик событий по нажатию, который передает 2
        ball = QPushButton("all")
        ball.clicked.connect(lambda: self._change_state_for_all(2))
        # обе кнопки добавляются в пользовательский интерфейс
        self.addWidget(ball)

    def _on_change(self):  # вызывается каждый раз, когда происходят изменения в модели
        if self._lock:
            return
        selected = set()
        for i in range(0, self._model.rowCount()):  # перебираем строки в таблице модели от 0 до количества строк в
            # модели
            if self._model.item(i, 0).checkState() != 0:  # если флаг установлен, то текст элемента добавляется в
                # множество selected
                selected.add(self._model.item(i, 0).text())
        self._selected = selected  # охраняем это множество
        for h in self._handlers:
            h(selected)

    def _change_state_for_all(self, mode):  # изменяет состояние флага для всех элементов модели
        self._lock = True
        for i in range(0, self._model.rowCount()):  # обходим все строки модели
            self._model.item(i, 0).setCheckState(mode)  # устанавливаем флаг в соответствии с mode
        self._lock = False
        self._on_change()

    @property
    def selected(self):  # геттер для переменной _selected
        return self._selected

    def connect(self, handler):  # добавляет обработчик в список
        self._handlers.append(handler)

    def try_load(self):  # загрузка данных
        pass

    def try_save(self):  # сохранение данных
        pass
