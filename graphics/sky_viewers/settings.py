from math import log10
from geometry.sky_math import sign


class ControllableSkySettings:  # класс, который сохраняет настройки
    # которые связаны с отображением изображения
    def __init__(self):
        self.second_per_second = 1
        self.zoom = 1

    @property
    def speed_rank(self): # ранг для скорости текущего объекта
        if self.second_per_second == 0:
            return 0
        return (log10(abs(self.second_per_second)) + 1) * sign(self.second_per_second)

    @speed_rank.setter
    def speed_rank(self, value):
        # автоматически вычисляет и изменяет
        # значение атрибута speed в соответствии с заданным значением.
        if value > 10:
            raise ValueError()
        self.second_per_second = 10 ** (abs(value) - 1) * sign(value)
        # новое значение атрибута second_per_second
        # в зависимости от значения атрибута speed_rank.
