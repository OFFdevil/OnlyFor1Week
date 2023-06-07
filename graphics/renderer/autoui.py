import datetime
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget


def trackable_setter(self, name, value):
    # функция для отслеживания изменений атрибутов объекта класса
    # с помощью вызова обработчиков handlers, когда значение атрибута меняется
    super(self.__class__, self).__setattr__(name, value)
    # super - чтобы получить доступ к методу, определенному в базовом классе,
    # чтобы передать значения self.class и name
    # setattr - чтобы обновить значения атрибута
    if name in self.handlers:  # есть ли у данного атрибута список обработчиков
        # handlers, которые реагируют на изменения атрибута (по-русски: проверяем, есть ли
        # список handlers, на который влияет наличие нового атрибута, если да,
        # то из списка функций вызываем всех со значением
        # нового параметра)
        for h in self.handlers[name]:
            h(value)


def trackable_object(obj):
    obj.handlers = {}  # атрибут = пустой словарь
    obj.__class__.__setattr__ = trackable_setter  # позволяет отслеживать
    # изменения атрибутов переданного объекта, путем вызова функций-обработчиков,
    # которые указаны в словаре
    return obj


def _create_edit_widget(data_parent, data_name: str, parser, builder) -> QLineEdit:
    widget = QLineEdit("")  # создаем/редактируем виджет

    def end_of_edit():
        try:
            value = parser(widget.text())
            if value is None:
                raise ValueError()
            data_parent.__setattr__(data_name, value)
            widget.setText(builder(value))
        except:
            widget.setText(builder(data_parent.__getattribute__(data_name)))

    widget.editingFinished.connect(end_of_edit)
    widget.handle = lambda: widget.setText(builder(data_parent.__getattribute__(data_name)))
    return widget


def _create_widget(parent: object, fname: str, ftype: type) -> QWidget:  # создаем виджет
    field = parent.__getattribute__(fname)
    if ftype == int or ftype == float or ftype == datetime:  # определили способ парсинга
        parser = fname if ftype != datetime else lambda s: datetime
        builder = str if type != datetime else lambda d: d.strftime(datetime_format)
        widget = _create_edit_widget(parent, parser, str)  # в итоге получили виджет, который может
        # редактировать атрибуты объекта


def _create_group(widget: QWidget, name: str) -> QLayout:  # создали группу элементов интерфейса
    # с 2мя виджетами - виджет и надпись
    layout = QGridLayout()  # сетка для размещения элементов в интерфейсе
    layout.addWidget(QLayout(name), 0, 0)  #добавили 2 элемента: надпись с именем и
    # виджет, который передан входным параметром
    layout.addWidget(widget, 0, 1)
    layout.handle = lambda: widget.update()
    return layout  # возвращает созданную группу виджетов


def get_object_widget(obj: object, fields, types):  # возвращает виджет для
    # редактирования объекта и его атрибутов
    if type(obj) == int or type(obj) == float or type(obj) == bool:
        # obj - то, для чего делаем виджет. В зависимости от типа решаем как редактировать
        raise TypeError('Primitive types unsupported!')
    layouts = []  # в этот список добавляем созданный виджет
    for fname in fields:  # для каждого поля создаем соответствующий виджет
        widget = _create_group(obj, fname)
        layouts += _create_group(widget, fname)
