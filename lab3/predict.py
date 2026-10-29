"""Файл predict.py — ЛР3, задание 2. Чтение кода: прогноз результата."""


class Counter:
    total = 0

    def __init__(self, name, start=0):
        self.name = name
        self.value = start
        Counter.total += 1

    def inc(self, step=1):
        self.value += step
        return self.value

    def __str__(self):
        return f"{self.name}: {self.value}"


a = Counter("A")
b = Counter("B", 10)
a.inc()
b.inc(5)
a.inc(a.value)
print(a, b, sep=" | ")                      # print 1
print(Counter.total, a.total)               # print 2
b.total = 100
print(Counter.total, b.total, a.total)      # print 3
c = a
c.inc()
print(a.value, c.value, a is c)             # print 4
print(Counter("X", 7).inc(3), Counter.total)   # print 5
