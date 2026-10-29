"""Файл predict.py — ЛР4, задание 2. Чтение кода с наследованием."""


class Device:
    count = 0

    def __init__(self, name):
        self.name = name
        Device.count += 1

    def info(self):
        return f"Устройство {self.name}"

    def kind(self):
        return "базовое"


class Camera(Device):
    def __init__(self, name, mp):
        super().__init__(name)
        self.mp = mp

    def info(self):
        return super().info() + f", камера {self.mp} Мп"


class Sensor(Device):
    def kind(self):
        return "датчик"


d = Device("D1")
c = Camera("C1", 12)
s = Sensor("S1")
print(d.info())                                         # print 1
print(c.info())                                         # print 2
print(s.info(), "|", s.kind(), "|", c.kind())           # print 3
print(Device.count, Camera.count)                       # print 4
print(isinstance(c, Device), isinstance(d, Camera),
      issubclass(Sensor, Camera))                       # print 5
print(type(s).__name__, type(s).__bases__[0].__name__)  # print 6
