class Horizontal:
    def __init__(self, a, d):
        self._a = a
        self._d = d

    @property  # геттер. возвращает угол a
    def a(self):
        return self._a

    @property  # геттер. возвращает d
    def d(self):
        return self._d

    def __str__(self):  # выводит a, d в заданном формате
        return "({}, {})".format(self.a, self.d)

    def __eq__(self, other):  # проверка равны ли параметры a d у текущего вектора и other
        return self.a == other.a and self.d == other.d
