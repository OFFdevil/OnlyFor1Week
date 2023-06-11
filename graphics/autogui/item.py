from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QGroupBox


# устанавливаем главный макет окна:
# Самый универсальный класс макета – это сеточный макет.
# Этот макет делит пространство на строки и столбцы.
# Чтобы создать сеточный макет, мы используем класс QGridLayout.
class Item(QGroupBox):
    def __init__(self, flat: bool = True):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        if flat:
            self.setFlat(True)
            self.setStyleSheet("border:1;")

    def try_save(self):
        raise NotImplementedError()

    def try_load(self):
        raise NotImplementedError()
