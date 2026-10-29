"""main.py — демонстрационная программа ЛР5 (задания 3–8). Вариант 3."""

from models import Account, AdminAccount, GuestAccount, ServiceToken, Asset


def line(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------- Задание 3: полиморфный метод risk_score() ----------
line("Задание 3. Полиморфный метод risk_score()")
acc = Account("user-ivanov", 1000, 400, True)
adm = AdminAccount("admin-ivanov", 2000, 1000, True, 2)
gst = GuestAccount("guest-petrov", 500, 450, True, 10)
print(acc, "->", acc.risk_score())     # round(400/1000*10) = 4
print(adm, "->", adm.risk_score())     # база round(1000/2000*10)=5 + 5*2 = 15
print(gst, "->", gst.risk_score())     # база round(450/500*10)=9 + 2 = 11
# Ручная проверка для guest с days_left = 0:
gst0 = GuestAccount("guest-zero", 1000, 100, True, 0)
print(gst0, "->", gst0.risk_score())   # база round(100/1000*10)=1 + 8 = 9

# ---------- Задание 4: единообразная обработка ----------
line("Задание 4. Функции report() и find_max()")


def report(items):
    """Выводит каждый объект и его risk_score(); возвращает сумму.
    Проверок типа нет — у всех объектов есть risk_score() (полиморфизм)."""
    total = 0
    n = 0
    for item in items:
        n += 1
        score = item.risk_score()       # версия выбирается по объекту
        print(f"{n}. {item} -> {score}")
        total += score
    avg = round(total / n, 2)
    print(f"Сумма: {round(total, 2)}, среднее: {avg}")
    return total


def find_max(items):
    """Возвращает объект с наибольшим risk_score() (циклом, без max)."""
    best = items[0]
    for item in items[1:]:
        if item.risk_score() > best.risk_score():
            best = item
    return best


mixed = [
    Account("user-ivanov-a", 1000, 900, True),
    AdminAccount("admin-ivanov-b", 4000, 2000, True, 3),
    GuestAccount("guest-petrov-c", 500, 100, True, 5),
    Account("user-ivanov-d", 2000, 0, False),
    AdminAccount("admin-ivanov-e", 8000, 6000, True, 1),
    GuestAccount("guest-petrov-f", 1000, 999, True, 0),
]
total = report(mixed)
print("Максимум:", find_max(mixed))

# ---------- Задание 5: сравнение объектов ----------
line("Задание 5. __eq__, __lt__, sorted/min/max")
print("sorted по used_mb:")
for obj in mixed:
    print("  ", obj.login, "-", obj.used_mb, "МБ")
print()
for obj in sorted(mixed):
    print("  ", obj.login, "-", obj.used_mb, "МБ")
print("min:", min(mixed).login, "| max:", max(mixed).login)

x = Account("user-x", 1000, 300, True)
y = Account("user-y", 2000, 300, False)
print("x == y:", x == y, "| x is y:", x is y)   # одинаковый ключ, разные объекты
try:
    print("x > y:", x > y)                       # требует __gt__ — его нет?
except TypeError as e:
    print("Ошибка в x > y:", e)
print("x <= y:", x <= y)                          # работает: добавлен __le__

# ---------- Задание 6: «утинная» типизация ----------
line("Задание 6. ServiceToken и утиная типизация")
duck_items = mixed + [ServiceToken("token-ivanov")]
total2 = report(duck_items)                      # функция работает без изменений
try:
    sorted(duck_items)                           # посторонний не поддерживает <
except TypeError as e:
    print("Ошибка сортировки со сторонним объектом:", e)

# ---------- Задание 7: абстрактный класс ----------
line("Задание 7. Абстрактный класс Asset")
try:
    a = Asset()                       # абстрактный класс — объекты не создаются
except TypeError as e:
    print("Ошибка создания Asset():", e)


class Draft(Asset):
    """Класс с реализованным только __str__ — создать объект нельзя."""

    def __str__(self):
        return "Черновик актива"


try:
    Draft()
except TypeError as e:
    print("Ошибка создания Draft():", e)
print("Обычные объекты создаются: isinstance(acc, Asset) =", isinstance(acc, Asset))

# ---------- Задание 8 (по желанию): арифметика объектов ----------
line("Задание 8. __add__ / __radd__")
print("acc + adm =", acc + adm)
s = sum(mixed)                                   # sum вызывает 0 + a -> __radd__
print("sum(mixed) =", round(s, 2), "| report вернул:", round(total, 2))
