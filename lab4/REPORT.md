# Отчёт по ЛР № 4 «Практикум по ООП: наследование»

Группа 9СА-354, Мурашко Владимир Антонович, номер в журнале 18 → вариант № 3.
Иерархия: `Account` → `AdminAccount`, `GuestAccount`. Папка `lab4/`.

## Задание 2. Таблица прогноза (код с Device/Camera/Sensor)

| № print | Прогноз (до запуска) | Фактический вывод | Причина расхождения |
|---|---|---|---|
| 1 | `Устройство D1` | `Устройство D1` | нет |
| 2 | `Устройство C1, камера 12 Мп` | так же | нет |
| 3 | `Устройство S1 \| датчик \| базовое` | так же | нет |
| 4 | `3 3` | `3 3` | нет |
| 5 | `True False False` | `True False False` | нет |
| 6 | `Sensor Device` | `Sensor Device` | нет |

Пояснения:
* print 3: у `Sensor` переопределён только `kind()`, метод `info()` унаследован от `Device`;
  `c.kind()` — не переопределён в `Camera`, берётся из базы («базовое»).
* print 4: `Camera.count` находит атрибут класса `Device.count = 3` (атрибуты класса
  наследуются; общего счётчика достаточно).
* print 5: `isinstance(c, Device)` — True (наследник); объект базы не является Camera;
  `Sensor` не является подклассом `Camera` — они «братья».

**Что изменится, если в Camera удалить `super().__init__(name)`?**
Конструктор родителя не вызовется: поле `self.name` не создастся, а `Device.count`
не увеличится. `print(c.info())` (print 2) вызвал бы `AttributeError: 'Camera' object
has no attribute 'name'`, а в print 4 было бы `2 3`... точнее `Device.count` стало бы 2.
Проверено временным удалением строки: программа падает на `c.info()` с AttributeError.

## Задания 3–5. Классы (`lab4/models.py`)

Схема иерархии:

```
┌─────────────────────────────┐
│ Account                     │
│ - count, kind               │
│ login, quota_mb,            │
│ _used_mb, active            │
│ + upload(mb)                │
│ + free_percent()            │
│ + __str__()                 │
└────────────▲────────────────┘
        ┌────┴─────┬──────────┐
┌───────┴────────┐ ┌──────────┴───────────┐
│ AdminAccount   │ │ GuestAccount         │
│ kind="Админ"   │ │ kind="Гость"         │
│ level          │ │ days_left            │
│ + raise_level()│ │ + extend(days)       │
│ + __str__()    │ │ + __str__()          │
└────────────────┘ └──────────────────────┘
```

* Оба подкласса вызывают `super().__init__(...)` — проверки базового класса работают
  и для наследников (показано в main: `GuestAccount("", 500, ...)` → ValueError про login).
* `__str__` подклассов расширяют родительский через `super().__str__()` (без копирования),
  название типа выводится благодаря атрибуту класса `kind`, переопределённому в наследниках.

## Задание 6. Таблица isinstance / issubclass

| № | Выражение | Прогноз | Результат |
|---|---|---|---|
| 1 | isinstance(s1, Account) | True | True |
| 2 | isinstance(b, AdminAccount) | False | False |
| 3 | isinstance(s2, AdminAccount) | False (s2 — GuestAccount) | False |
| 4 | issubclass(GuestAccount, Account) | True | True |
| 5 | issubclass(Account, Account) | True (класс — подкласс себя) | True |
| 6 | type(s1) == Account | False | False |
| 7 | AdminAccount.__bases__ | (Account,) | `(<class 'models.Account'>,)` |
| 8 | AdminAccount.__mro__ | AdminAccount, Account, object | `(AdminAccount, Account, object)` |
| 9 | Account.count после b, s1, s2 | 3 (+объекты раньше) | 4 (с учётом объектов до задания 6) |
| 10 | вызов raise_level() у объекта b | ошибка | `AttributeError - 'Account' object has no attribute 'raise_level'` |

Разница строк 1 и 6: `isinstance` учитывает наследников (s1 — объект AdminAccount,
который *является* Account → True), а `type(s1) == Account` сравнивает точный тип
объекта — type(s1) есть AdminAccount, поэтому False.
Ошибка в строке 10: метод `raise_level` объявлен только в AdminAccount; у объекта базового
класса его нет — Python поднимается по MRO (Account → object) и не находит метод.

## Вывод программы (задание 7)

```

============================================================
Задание 7. Список объектов иерархии
============================================================
Учётная запись user-ivanov-1: занято 300 из 2000 МБ, запись активна.
Администратор admin-ivanov-1: занято 1000 из 4000 МБ, запись активна, уровень: 1.
   raise_level() -> 2
Администратор admin-ivanov-2: занято 200 из 8000 МБ, запись не активна, уровень: 3.
   raise_level(): ошибка - Достигнут предел: максимальный уровень 3
Гость guest-petrov-1: занято 400 из 500 МБ, запись активна, осталось дней: 25.
   extend(1) -> 26
Гость guest-petrov-2: занято 0 из 1000 МБ, запись активна, осталось дней: 5.
   extend(1) -> 6
Подсчёт объектов по классам: {'Account': 1, 'AdminAccount': 2, 'GuestAccount': 2}
Account.count (весь запуск программы) = 9
```

## Выводы

Наследование позволяет строить классы-частные случаи без дублирования кода: AdminAccount
и GuestAccount получили все поля, проверки и методы Account, добавив по одному полю и методу.
Вызов `super().__init__()` обязателен — без него поля родителя не заполняются.
Переопределение `__str__` с расширением через `super().__str__()` удобнее полной замены.
Функции `isinstance`/`issubclass` и атрибуты `__bases__`, `__mro__` наглядно показывают
отношения в иерархии; атрибут класса `count` общий для всех наследников.
