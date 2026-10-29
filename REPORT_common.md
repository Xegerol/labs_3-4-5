# Отчёт по практикуму по ООП (ЛР № 3, 4, 5)

**Дисциплина:** Программирование / Объектно-ориентированное программирование
**Студент:** Мурашко Владимир Антонович
**Группа:** 9СА-354
**Номер в журнале:** 18 → **Вариант:** № 3 — класс **Account (учётная запись)** во всех трёх работах.

Иерархия классов по варианту 3:

```
        Account                     (ЛР3: базовый класс)
       /      \
AdminAccount   GuestAccount         (ЛР4: наследники)
```

Поля базового класса `Account`: `login` (str, непустая), `quota_mb` (int, 100–10000),
`used_mb` (int, 0–quota_mb), `active` (bool). Метод-изменение `upload(mb)`,
расчётный метод `free_percent()`, инкапсулируемое поле — `used_mb` (задание 6 ЛР3).

Подклассы:
* `AdminAccount` + поле `level` (int, 1–3), метод `raise_level()`;
* `GuestAccount` + поле `days_left` (int, 0–30), метод `extend(days)`.

Полиморфный метод (ЛР5): `risk_score()` — базовый `round(used_mb / quota_mb · 10)`,
AdminAccount: `базовая + 5·level`, GuestAccount: `базовая + 2, если days_left > 0, иначе базовая + 8`.
Ключ сравнения: `used_mb`. Посторонний класс: `ServiceToken(name) → 7`.

Структура проекта в репозитории:

```
oop-python-murashko/
├── README.md
├── lab3/  models.py, main.py, predict.py, bugfix.py
├── lab4/  models.py, main.py, predict.py
└── lab5/  models.py, main.py, predict.py
```

> Примечание: ссылка на GitHub — `https://github.com/<логин>/oop-python-murashko`
> (ветка `murashko-3`). В коде имена объектов содержат фамилии-примеры (`ivanov`, `petrov`).
