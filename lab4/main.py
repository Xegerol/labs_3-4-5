"""main.py — демонстрационная программа ЛР4 (задания 3–7). Вариант 3."""

from models import Account, AdminAccount, GuestAccount


def line(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------- Задание 3: первый подкласс AdminAccount ----------
line("Задание 3. Подкласс AdminAccount")
adm = AdminAccount("admin-ivanov", 4000, 1000, True, 2)
print(adm)
adm.upload(500)                      # унаследованный метод-изменение из ЛР3
print("После upload(500):", adm)
print("free_percent():", adm.free_percent())   # унаследованный расчётный метод
print("raise_level() ->", adm.raise_level())   # собственный метод
try:
    bad_a = AdminAccount("admin-max", 4000, 0, True, 3)
    bad_a.raise_level()              # ошибочный вызов собственного метода
except ValueError as e:
    print("Ошибка:", e)

# ---------- Задание 4: второй подкласс GuestAccount ----------
line("Задание 4. Подкласс GuestAccount")
g = GuestAccount("guest-petrov", 500, 100, True, 10)
print(g)
print("extend(5) ->", g.extend(5))   # собственный метод
try:
    g.extend(-2)
except ValueError as e:
    print("Ошибка:", e)
try:
    g.extend(99)                     # итог больше 30 дней
except ValueError as e:
    print("Ошибка:", e)
try:
    # ошибка в поле БАЗОВОГО класса обнаруживается при создании подкласса
    bad_g = GuestAccount("", 500, 0, True, 5)
except ValueError as e:
    print("Ошибка базового поля:", e)

# ---------- Задание 5: переопределение __str__ ----------
line("Задание 5. __str__ с названием типа")
b = Account("user-ivanov", 2000, 300, True)
print(b)
print(adm)
print(g)

# ---------- Задание 6: исследование иерархии ----------
line("Задание 6. isinstance / issubclass / __mro__")
s1 = adm
s2 = g
print("1. isinstance(s1, Account)          =", isinstance(s1, Account))
print("2. isinstance(b, AdminAccount)      =", isinstance(b, AdminAccount))
print("3. isinstance(s2, AdminAccount)     =", isinstance(s2, AdminAccount))
print("4. issubclass(GuestAccount, Account) =", issubclass(GuestAccount, Account))
print("5. issubclass(Account, Account)     =", issubclass(Account, Account))
print("6. type(s1) == Account              =", type(s1) == Account)
print("7. AdminAccount.__bases__           =", AdminAccount.__bases__)
print("8. AdminAccount.__mro__             =", AdminAccount.__mro__)
print("9. Account.count после b, s1, s2    =", Account.count)
print("10. Вызов raise_level() у объекта базового класса b:")
try:
    b.raise_level()
except AttributeError as e:
    print("    ", type(e).__name__, "-", e)

# ---------- Задание 7: демонстрация со списком объектов ----------
line("Задание 7. Список объектов иерархии")
objects = [
    Account("user-ivanov-1", 2000, 300, True),
    AdminAccount("admin-ivanov-1", 4000, 1000, True, 1),
    AdminAccount("admin-ivanov-2", 8000, 200, False, 3),
    GuestAccount("guest-petrov-1", 500, 400, True, 25),
    GuestAccount("guest-petrov-2", 1000, 0, True, 5),
]
for obj in objects:
    print(obj)
    if isinstance(obj, AdminAccount):
        try:
            print("   raise_level() ->", obj.raise_level())
        except ValueError as e:
            print("   raise_level(): ошибка -", e)
    elif isinstance(obj, GuestAccount):
        try:
            print("   extend(1) ->", obj.extend(1))
        except ValueError as e:
            print("   extend(1): ошибка -", e)

counts = {}
for obj in objects:
    name = type(obj).__name__
    counts[name] = counts.get(name, 0) + 1
print("Подсчёт объектов по классам:", counts)
print("Account.count (весь запуск программы) =", Account.count)
