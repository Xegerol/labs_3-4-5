"""bugfix.py — ЛР3, задание 8 (повышенной сложности). Поиск ошибок в классе.

Найдено 8 ошибок (не менее шести требовалось):
1. class Thermometer                      -> пропущено двоеточие в конце строки.
2. def __init__(name, value):             -> нет параметра self.
3. def set_value(self, value): ...        -> при ошибке только print(), а нужно
   генерировать исключение ValueError (иначе объект остаётся в неверном состоянии).
4. value = self.value                     -> перепутано направление присваивания;
   должно быть self.value = value.
5. def to_fahrenheit():                   -> нет параметра self, метод не может
   обратиться к self.value.
6. return self.value * 9 / 5 + 32         -> синтаксически верно, но unit в f-строке
   __str__ обращён к глобальной переменной, а не к атрибуту класса.
7. print(f"...") в __str__                -> __str__ обязан возвращать строку
   (return), а не печатать её.
8. {unit}                                 -> должно быть {Thermometer.unit}
   (или self.unit); имя unit без префикса вне класса не определено...
   (внутри __str__ it NameError).
"""


class Thermometer:                                    # исправлено 1
    unit = "C"

    def __init__(self, name, value):                  # исправлено 2
        self.name = name
        self.set_value(value)                         # проверка через тот же метод

    def set_value(self, value):
        if value < -50 or value > 50:
            raise ValueError(f"value = {value}: допустимо от -50 до 50")  # испр. 3
        self.value = value                            # исправлено 4

    def to_fahrenheit(self):                          # исправлено 5
        return self.value * 9 / 5 + 32

    def __str__(self):
        return f"{self.name}: {self.value} {Thermometer.unit}"  # исправлено 6, 7, 8


if __name__ == "__main__":
    t = Thermometer("t-ivanov", 20)
    print(t)
    t.set_value(25)                                   # корректное изменение
    print(t, "->", round(t.to_fahrenheit(), 1), "F")
    try:
        t.set_value(100)                              # некорректное значение
    except ValueError as e:
        print("Ошибка:", e)
