from datetime import datetime
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget


# QImage - класс для обработки данных изображения
# QPainter - класс для отрисовки
class ImageViewer(QWidget):  # класс, отвечающий за просмотр изображения
    def __init__(self):
        super().__init__()
        self._image = QImage(self.size(), QImage.Format_RGB32)  # создаем изображение по размеру и цветовому формату
        self.setMouseTracking(True)
        self.out_file_name = 'sky.jpg'

    @property
    def image(self):  # геттер
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self.repaint()  # перерисовывает прямоугольник внутри виджета

    def save_to_file(self):
        self.image.save(datetime.now().strftime(self.out_file_name))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)  # начинает рисование и возвращает тру если успешно
        painter.drawImage(0, 0, self.image)  # рисует
        painter.end()  # заканчивает рисование и возвращает тру если успешно

    def resizeEvent(self,
                    event):  # возвращает копию изображения, масштабированного до прямоуголоника с заданными размерами
        self.image = self.image.scaled(self.size())
