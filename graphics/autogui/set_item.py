from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QModelIndex
from graphics.autogui.cast_tools import to_widget
from graphics.autogui.item import Item


# создаем класс, который наследуется от Item
class CheckBoxSet(Item):
    def __init__(self, str_set, selected, handler=None):
        super().__init__()
        self._src = set(str_set)  # в переменную сохраняем все множество значений, переданных в str_set
        self._selected = set(str_set)
        self._handlers = [] if handler is None else [handler]  # пустой список или передается обработчик, если handler
        # не был передан
        self._create_widget()  # методы создания виджетов и кнопок
        self._create_widget(selected)
        self._create_buttons()

    def _create_widget(self, selected):
        self._model = QStandardItemModel()  # используем модель, которая будет хранить данные списка элементов
        for row in sorted(self._src):
            item = QStandardItem(row)  # для каждого элемента создаем экземпляр, который содержит текст элемента и
            # устанавливает флажок, начальное состояние
            item.setCheckState(2 if row in selected else 0)
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

        self._widget.doubleClicked.connect(self._on_double_press)
        self.layout.addWidget(self._widget)

    def _on_double_press(self):  # обработка двойного нажатия на элемент списка из виджета
        try:
            i = self._model.item(self._widget.currentIndex().row())
            txt = i.text()
        except:
            return
        self.on_double_press(txt)

    def on_double_press(self, text: str):
        pass

    def _create_buttons(self):
        buttons = QGridLayout()  # создаем кнопку- сеточный макет
        buttons.setSpacing(0)  # устанавливаем интервалы = 0 по вертикали и горизонтали
        buttons.setContentsMargins(0, 0, 0, 0)  # устанавливаем поля
        # создаем кнопку none, обработчик событий по нажатию, который передает 0
        bclear = QPushButton("none")
        bclear.clicked.connect(lambda: self._change_state_for_all(0))
        buttons.addWidget(bclear, 0, 0)
        # создаем кнопку all, обработчик событий по нажатию, который передает 2
        ball = QPushButton("all")
        ball.clicked.connect(lambda: self._change_state_for_all(2))
        # обе кнопки добавляются в пользовательский интерфейс
        buttons.addWidget(ball, 0, 1)
        self.layout.addWidget(to_widget(buttons))  # переводим кнопку в виджет и добавляем в макет

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
