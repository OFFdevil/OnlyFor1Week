from math import sqrt


class NVector:
    def __init__(self, dimensions):  # создаем объект класса по заданным координатам
        self._items = tuple(dimensions)  # храним координаты
        self._rank = len(self._items)  # и размерность

    @property
    def rank(self):
        return self._rank

    @property
    def length(self):  # считаем длину вектора
        s = 0
        for i in self:
            s += i ** 2
        return sqrt(s)

    def __getitem__(self, index):  # возвращает координату номера index
        return self._items[index]

    # next & iter - для итерации по координатам вектора, как по контейнеру
    def __next__(self):
        for i in self._items:
            yield i

    def __iter__(self):
        for i in self._items:
            yield i

    # перегрузка арифметических функций
    def _add_(self, other):
        v = []
        for i in range(0, self.rank):
            v.append(self[i] + other[i])
        return NVector(v)

    def _mul_(self, other):  # умножаем каждую компоненту вектора на переданный параметр
        v = []
        for i in range(0, self.rank):
            v.append(self[i] * other)
        return NVector(v)

    def _sub_(self, other):  # вычитание
        return self._add_(other._mul_(-1))

    def __str__(self):  # преобразование в строку
        s = "("
        for i in self:
            s += str(i) + ', '
        return s[:-2] + ')'

    def __hash__(self):
        h = 0
        for i in self:  # XOR
            h ^= hash(i)
        return h

    def __eq__(self, other):  # определяет равны объекты или нет
        if self.rank != other.rank:
            return False
        for i in range(0, self.rank):
            if self[i] != other[i]:
                return False
        return True
