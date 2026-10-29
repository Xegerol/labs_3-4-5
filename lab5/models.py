"""models.py — ЛР5. Иерархия Account/AdminAccount/GuestAccount + полиморфизм, abc."""

from abc import ABC, abstractmethod


class Asset(ABC):
    """Абстрактный базовый класс любого объекта учёта: объект обязан уметь
    вычислять свой показатель риска и описывать себя строкой."""

    @abstractmethod
    def risk_score(self):
        """Показатель риска по заполнению квоты (0..10 и выше)."""

    @abstractmethod
    def __str__(self):
        """Человекочитаемое описание объекта."""


class Account(Asset):
    """Учётная запись пользователя на файловом сервере: логин, выделенная
    квота места, занятое место и признак активности записи."""

    count = 0                      # атрибут класса — счётчик созданных объектов
    kind = "Учётная запись"        # название типа для __str__ (ЛР4, задание 5)

    def __init__(self, login, quota_mb, used_mb, active):
        if login == "":
            raise ValueError(f"login = '{login}': логин не может быть пустым")
        if not isinstance(quota_mb, int) or quota_mb < 100 or quota_mb > 10000:
            raise ValueError(f"quota_mb = {quota_mb}: допустимо от 100 до 10000")
        self.quota_mb = quota_mb    # квота проверена, поле нужно сеттеру used_mb
        # проверка used_mb выполняется свойством (задание 6), сеттер вызывает ValueError
        self.used_mb = used_mb      # обращение через свойство -> сработает сеттер
        if not isinstance(active, bool):
            raise ValueError(f"active = {active}: ожидается True или False")
        self.login = login
        self.active = active
        Account.count += 1          # счётчик увеличиваем только если ошибок не было

    # ---- задание 6 (ЛР3): инкапсуляция поля used_mb --------------------
    @property
    def used_mb(self):             # чтение: acc.used_mb
        return self._used_mb

    @used_mb.setter
    def used_mb(self, value):      # запись: acc.used_mb = 500
        if not isinstance(value, int) or value < 0 or value > self.quota_mb:
            raise ValueError(
                f"used_mb = {value}: допустимо от 0 до {self.quota_mb} (квота)")
        self._used_mb = value

    # ---- методы из ЛР3 ----------------------------------------------------
    def upload(self, mb):
        """Метод-изменение: добавляет mb к занятому месту.
        mb > 0, данные должны помещаться в квоту, запись должна быть активна."""
        if not isinstance(mb, int) or mb <= 0:
            raise ValueError(f"mb = {mb}: объём загрузки должен быть больше 0")
        if not self.active:
            raise ValueError("Нельзя записать данные: учётная запись не активна")
        free = self.quota_mb - self.used_mb
        if mb > free:
            raise ValueError(
                f"mb = {mb}: не хватает свободного места (свободно {free} МБ)")
        self.used_mb = self.used_mb + mb   # изменение через свойство (проверка сеттера)

    def free_percent(self):
        """Расчётный метод: свободное место в процентах, округлённое до 0,1."""
        return round((self.quota_mb - self.used_mb) / self.quota_mb * 100, 1)

    def __str__(self):
        status = "активна" if self.active else "не активна"
        return (f"{self.kind} {self.login}: занято {self.used_mb} из "
                f"{self.quota_mb} МБ, запись {status}.")

    # ---- ЛР5, задание 3: полиморфный метод ------------------------------
    def risk_score(self):
        """Базовый риск: round(used_mb / quota_mb * 10)."""
        return round(self.used_mb / self.quota_mb * 10)

    # ---- ЛР5, задание 5: сравнение по ключу used_mb ---------------------
    def __eq__(self, other):
        return self.used_mb == other.used_mb

    def __lt__(self, other):
        return self.used_mb < other.used_mb

    def __le__(self, other):
        return self.used_mb <= other.used_mb

    # ---- ЛР5, задание 8 (по желанию): арифметика объектов ---------------
    def __add__(self, other):
        """a + b -> сумма показателей риска двух записей."""
        return self.risk_score() + other.risk_score()

    def __radd__(self, other):
        """Нужен для sum([obj1, obj2, ...]): sum начинает с 0 + obj1."""
        return other + self.risk_score()


class AdminAccount(Account):
    """Административная учётная запись — частный случай учётной записи:
    у неё есть уровень привилегий (1–3), повышающий показатель риска."""

    kind = "Администратор"         # переопределяем название типа для __str__

    def __init__(self, login, quota_mb, used_mb, active, level):
        super().__init__(login, quota_mb, used_mb, active)  # поля/проверки родителя
        if not isinstance(level, int) or level < 1 or level > 3:
            raise ValueError(f"level = {level}: допустимо от 1 до 3")
        self.level = level

    def raise_level(self):
        """Собственный метод: повышает уровень привилегий на 1; при 3 — ошибка."""
        if self.level >= 3:
            raise ValueError("Достигнут предел: максимальный уровень 3")
        self.level += 1
        return self.level

    def __str__(self):
        return super().__str__()[:-1] + f", уровень: {self.level}."

    def risk_score(self):
        """ЛР5: базовый риск + 5 за каждый уровень привилегий."""
        return round(super().risk_score() + 5 * self.level)


class GuestAccount(Account):
    """Гостевая учётная запись — частный случай учётной записи: временная,
    срок её действия влияет на оценку риска."""

    kind = "Гость"                 # переопределяем название типа для __str__

    def __init__(self, login, quota_mb, used_mb, active, days_left):
        super().__init__(login, quota_mb, used_mb, active)  # поля/проверки родителя
        if not isinstance(days_left, int) or days_left < 0 or days_left > 30:
            raise ValueError(f"days_left = {days_left}: допустимо от 0 до 30")
        self.days_left = days_left

    def extend(self, days):
        """Собственный метод: продлевает срок на days дней (days > 0, итог не более 30)."""
        if not isinstance(days, int) or days <= 0:
            raise ValueError(f"days = {days}: продление должно быть больше 0")
        total = self.days_left + days
        if total > 30:
            raise ValueError(
                f"days = {days}: итог {total} превышает предел 30 дней")
        self.days_left = total
        return self.days_left

    def __str__(self):
        return super().__str__()[:-1] + f", осталось дней: {self.days_left}."

    def risk_score(self):
        """ЛР5: базовый риск + 2, если срок ещё остался, иначе + 8."""
        if self.days_left > 0:
            return round(super().risk_score() + 2)
        return round(super().risk_score() + 8)


class ServiceToken():
    """ЛР5, задание 6: «посторонний» класс для утиной типизации.
    Не наследует ни один класс иерархии, но имеет risk_score() и __str__."""

    def __init__(self, name):
        self.name = name

    def risk_score(self):
        return 7

    def __str__(self):
        return f"Сервисный токен «{self.name}»"
