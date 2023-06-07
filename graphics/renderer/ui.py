import datetime

from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit


# TODO: set focus?
# TODO: auto change value, after modigy in parent (use decorator)
def __end_of_edit(parser, builder, widget: QLineEdit, data_parent, data_name: str, nonable: bool):
    # событие завершения редактирования
    try:
        value = parser(widget.text())  # попытка парсинга текста
        if value is None:
            raise ValueError()  # если парсинг не удался
        data_parent.__setattr__(data_name, value)  # если парсинг прошел успешно, то
        # значение сохраняется в атрибут data_parent
        widget.setText(builder(value))  # отображается в QLineEdit с помощью
        # builder
    except:
        widget.setText(builder(data_parent.__getattribute__(data_name)))


def _create_widget(data_parent, data_name: str, parser, builder, nonable: bool) -> QLineEdit:
    widget = QLineEdit(builder(data_parent.__getattribute__(data_name)))  # создали виджет
    widget.editingFinished.connect(lambda: __end_of_edit(parser, builder, widget, data_parent, data_name, nonable))
    # окончание редактирования виджета
    return widget  # возвращает виджет, который готов к использованию


def _on_change(w: QCheckBox, data_parent, data_name):  #
    # характеризует изменение
    # списка (где надо ставить галочки)
    data_parent.__setattr__(data_name, w.checkState())


def create_bool_widget(name: str, data_parent, data_name: str) -> QCheckBox:
    # создает виджет QCheckBox для булевого значения,
    # связывает его с методом `_on_change` для отслеживания изменений значения
    box = QCheckBox(name)  # флажок
    box.setChecked(data_parent.__getattribute__(data_name))  # есть галочка или нет
    box.stateChanged.connect(lambda: _on_change(box, data_parent, data_name))
    return box  # возвращает созданный виджет.


def create_float_widget(data_parent, data_name: str) -> QLineEdit:
    # функция для редактирования значения вещественного атрибута объекта
    return _create_widget(data_parent, data_name, float, str, False)


def create_datetime_widget(data_parent, data_name: str, datetime_format: str) -> QLineEdit:
    # создаем виджет, который используется для ввода даты и времени
    parser = lambda s: datetime.datetime.strptime(s, datetime_format)  # возвращает дату и время
    builder = lambda d: d.strftime(datetime_format)  # возвращает строку datetime_format
    return _create_widget(data_parent, data_name, parser, builder, False)  # возвращает созданный виджет
