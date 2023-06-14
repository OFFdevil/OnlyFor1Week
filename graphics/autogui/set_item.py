from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QPushButton
from graphics.autogui.cast_tools import to_widget
from graphics.autogui.item import Item


class CheckBoxSet(Item):
    def __init__(self, str_set, selected, handler=None):
        super().__init__()
        self._src = set(str_set)
        self._selected = set(str_set)
        self._handlers = [] if handler is None else [handler]
        self._create_widget(selected)
        self._create_buttons()

    def _create_widget(self, selected):
        self._model = QStandardItemModel()
        for row in sorted(self._src):
            item = QStandardItem(row)
            item.setCheckState(2 if row in selected else 0)
            item.setCheckable(True)
            item.setEditable(False)
            self._model.appendRow(item)

        view = QListView()
        view.setModel(self._model)
        view.clicked.connect(lambda: self._on_change())
        self._model.itemChanged.connect(lambda: self._on_change())

        self._lock = False
        self._widget = view
        self._widget.doubleClicked.connect(self._on_double_press)
        self.layout.addWidget(self._widget)

    def _on_double_press(self):
        try:
            i = self._model.item(self._widget.currentIndex().row())
            txt = i.text()
        except:
            return
        self.on_double_press(txt)

    def on_double_press(self, text: str):
        pass

    def _create_buttons(self):
        buttons = QGridLayout()
        buttons.setSpacing(0)
        buttons.setContentsMargins(0, 0, 0, 0)
        bclear = QPushButton("none")
        bclear.clicked.connect(lambda: self._change_state_for_all(0))
        buttons.addWidget(bclear, 0, 0)
        ball = QPushButton("all")
        ball.clicked.connect(lambda: self._change_state_for_all(2))
        buttons.addWidget(ball, 0, 1)
        self.layout.addWidget(to_widget(buttons))

    def _on_change(self):
        if self._lock:
            return
        selected = set()
        for i in range(0, self._model.rowCount()):
            # модели
            if self._model.item(i, 0).checkState() != 0:
                selected.add(self._model.item(i, 0).text())
        self._selected = selected
        for h in self._handlers:
            h(selected)

    def _change_state_for_all(self, mode):
        self._lock = True
        for i in range(0, self._model.rowCount()):
            self._model.item(i, 0).setCheckState(mode)
        self._lock = False
        self._on_change()

    @property
    def selected(self):
        return self._selected

    def connect(self, handler):
        self._handlers.append(handler)

    def try_load(self):
        pass

    def try_save(self):
        pass
