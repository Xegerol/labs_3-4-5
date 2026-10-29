"""models.py — ЛР3, задания 3–6. Вариант № 3 (журнал 18): класс Account."""


class Account:
    """Учётная запись пользователя на файловом сервере: логин, выделенная
    квота места, занятое место и признак активности записи."""

    count = 0                      # атрибут класса — счётчик созданных объектов

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

    # ---- задание 6: инкапсуляция поля used_mb ---------------------------
    @property
    def used_mb(self):             # чтение: acc.used_mb
        return self._used_mb

    @used_mb.setter
    def used_mb(self, value):      # запись: acc.used_mb = 500
        if not isinstance(value, int) or value < 0 or value > self.quota_mb:
            raise ValueError(
                f"used_mb = {value}: допустимо от 0 до {self.quota_mb} (квота)")
        self._used_mb = value

    # ---- задание 5: методы ----------------------------------------------
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
        return (f"Учётная запись {self.login}: занято {self.used_mb} из "
                f"{self.quota_mb} МБ, запись {status}.")
