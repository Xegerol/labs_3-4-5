"""Файл predict.py — ЛР5, задание 2. Полиморфизм и магические методы."""


class Shape:
    def area(self):
        return 0

    def __str__(self):
        return f"{type(self).__name__}({self.area()})"


class Square(Shape):
    def __init__(self, a):
        self.a = a

    def area(self):
        return self.a * self.a

    def __lt__(self, other):
        return self.area() < other.area()


class Rect(Square):
    def __init__(self, a, b):
        super().__init__(a)
        self.b = b

    def area(self):
        return self.a * self.b


class Label:
    def area(self):
        return "нет площади"


items = [Rect(2, 5), Square(3), Shape(), Rect(1, 1)]
for x in items:
    print(x.area(), end=" ")
print()                                                # print 1 (вся строка)
print(Square(3) == Square(3), Square(2) < Rect(1, 5))  # print 2
print(*sorted([Rect(2, 5), Square(3), Rect(1, 1)]))    # print 3
print(Label().area())                                  # print 4
print(Rect(2, 3))                                      # print 5
