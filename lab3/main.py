"""main.py — демонстрационная программа ЛР3 (задания 3–7). Вариант 3 — Account."""

from models import Account


def line(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------- Задание 3: класс и конструктор ----------
line("Задание 3. Создание объектов и вывод полей")
acc1 = Account("ivanov", 2000, 500, True)
acc2 = Account("petrov", 1000, 0, False)

for a in (acc1, acc2):
    print(f"login={a.login!r}, quota_mb={a.quota_mb}, "
          f"used_mb={a.used_mb}, active={a.active}")
print("Счётчик объектов Account.count =", Account.count)

# ---------- Задание 4: проверка входных данных ----------
line("Задание 4. Проверка входных данных (ошибочные объекты)")
bad_data = [
    ("пустой login", lambda: Account("", 2000, 500, True)),
    ("quota_mb вне диапазона", lambda: Account("test-user", 50, 0, True)),
    ("used_mb больше квоты", lambda: Account("test-user", 1000, 1500, True)),
]
for comment, creator in bad_data:
    try:
        creator()
    except ValueError as e:
        print(f"Ошибка ({comment}): {e}")
print("Account.count после неудачных попыток =", Account.count,
      "(объекты не созданы, счётчик не вырос)")

# ---------- Задание 5: методы и __str__ ----------
line("Задание 5. Методы upload / free_percent и __str__")
print(acc1)                       # вызывается __str__
acc1.upload(300)                  # корректная загрузка
print("После upload(300):", acc1)
print("Свободное место:", acc1.free_percent(), "%")
try:
    acc1.upload(-10)              # ошибочное значение
except ValueError as e:
    print("Ошибка:", e)
try:
    acc2.upload(100)              # запись не активна
except ValueError as e:
    print("Ошибка:", e)
try:
    acc1.upload(5000)             # больше свободного места
except ValueError as e:
    print("Ошибка:", e)

# ---------- Задание 6: инкапсуляция (свойство used_mb) ----------
line("Задание 6. Свойство used_mb")
print("Чтение через свойство: acc1.used_mb =", acc1.used_mb)
acc1.used_mb = 800                # корректное присваивание
print("После acc1.used_mb = 800:", acc1.used_mb)
try:
    acc1.used_mb = -5             # некорректное присваивание
except ValueError as e:
    print("Ошибка:", e)
try:
    acc1.used_mb = 99999          # больше квоты
except ValueError as e:
    print("Ошибка:", e)

# ---------- Задание 7: итоговый объект и счётчик ----------
line("Задание 7. Третий объект и итоговое значение счётчика")
acc3 = Account("sidorov", 5000, 1200, True)
print(acc3)
print("Итоговый Account.count =", Account.count,
      "(3 успешных объекта; три неудачные попытки в задании 4 не засчитываются)")
