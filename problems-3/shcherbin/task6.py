# coding: utf8
import types
import math


class Vector:
    """Вектор линейной алгебры. Реализует операции умножения на константу при записи a*V,
     где a - константа V - вектор; При записи U*V выполняет операцию скалярного произведения,
     в данном случае U,V - векторы"""

    myVector = []

    @staticmethod
    def __getElemType(elements):
        validTypes = (int, float, complex)
        typeNumber = 0
        for elem in elements:
            try:
                ti = validTypes.index(type(elem))
                if typeNumber < ti:
                    typeNumber = ti
            except ValueError:
                try:
                    validTypes[typeNumber](elem)
                except (TypeError, ValueError):
                    typeNumber += 1

        return validTypes[typeNumber]

    def __init__(self, *args):
        """Создает vector из переданного iterable или чисел
        :param iterable
        """
        if len(args) == 1:
            if isinstance(*args, (tuple, list)):
                print("collection")
                t = self.__getElemType(*args)
                self.myVector = [t(e) for e in args[0]]
            if isinstance(*args, types.GeneratorType):
                print("generator")
                l = [e for e in args[0]]
                t = self.__getElemType(l)
                self.myVector = [t(e) for e in l]
            else:
                t = self.__getElemType(args)
                self.myVector = [t(*args)]
        else:
            t = self.__getElemType(args)
            self.myVector = [t(e) for e in args]

    def __len__(self) -> int:
        """
        :return: Количество элементов вектора
        """
        return len(self.myVector)

    def __setitem__(self, key, value):
        """
        Устанавливает указанное значение в указанную координату
        :param key: Номер координаты в векторе >= 0
        :param value: Значение в этой координате (число)
        """
        self.myVector[key] = value

    def __add__(self, other: "Vector") -> "Vector":
        """Операция сложения векторов
        :param other: Объект этого же класса Vector
        :return: Сумма векторов линейной алгебры (объект класса Vector)
        """
        return Vector([values[0] + values[1] for values in zip(self.myVector, other.myVector)])

    def __sub__(self, other):
        """Операция вычитания векторов
        :param other: Объект класса Vector
        :return: Разность векторов
        """
        return Vector([values[0] - values[1] for values in zip(self.myVector, other.myVector)])

    def __rmul__(self, other):
        """Операция умножения на константу справа
        :param other: Числовая константа
        :return: Вектор, умноженный на константу
        """
        return Vector([val * other for val in self.myVector])

    def __mul__(self, other):
        """Операция скалярного произведения для векторов и умножения на константу слева
        :param other: Объект класса Vector
        :return: Результат скалярного произведения векторов
        """
        if isinstance(other, Vector):
            if len(other) != len(self):
                raise TypeError
            return sum([val[0] * val[1] for val in zip(self.myVector, other.myVector)])
        if isinstance(other, (int, float, complex)):
            return Vector([val * other for val in self.myVector])

    def __eq__(self, other):
        """Проверка векторов на равенство
        :param other: Объект класса Vector
        :return: true если координаты векторов совпадают, false - иначе
        """
        return self.myVector == other.myVector

    def __getitem__(self, item):
        """Получение элемента по индексу
        :param item: Индекс(номер координаты вектора)
        :return: Число, находящееся в векторе по данному индексу
        """
        return self.myVector[item]

    def __str__(self):
        """Перевод в строку
        :return: Строковое представление вектора
        """
        return str(self.myVector)

    def get_length(self):
        """
        Вычисляет Евклидову длину вектора
        :return: Евклидова длина вектора
        """
        return math.sqrt(sum(v ** 2 for v in self.myVector))


class Vector3D(Vector):
    def __init__(self, *args):
        super().__init__(*args)
        if super().__len__() != 3:
            raise AttributeError

    def crossProduct(self, other):
        return Vector3D(self[1] * other[2] - self[2] * other[1],
                        self[2] * other[0] - self[0] * other[2],
                        self[0] * other[1] - self[1] * other[0])


if __name__ == '__main__':
    v = Vector(complex(3.5, 6))
    print(type(v[0]))
    print(v)
