from PyQt5.QtWidgets import QGridLayout


# устанавливаем главный макет окна:
# Самый универсальный класс макета – это сеточный макет.
# Этот макет делит пространство на строки и столбцы.
# Чтобы создать сеточный макет, мы используем класс QGridLayout.
class Item(QGridLayout):
    def __init__(self):
        super().__init__()

    def try_save(self):
        raise NotImplementedError()

    def try_load(self):
        raise NotImplementedError()
