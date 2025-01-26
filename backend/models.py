from django.db import models


class StorageBox(models.Model):
    VOLUME_CHOICES = [
        ("Small", "Маленькая: 1 m^3"), ("Medium",
                                        "Средняя: 1-3 m^3"), ("Large", "Большая: >5 m^3")
    ]
    name = models.CharField(
        max_length=150, verbose_name="Имя Склада", null=True)

    description = models.TextField(
        null=True, blank=True, verbose_name="Описание")
    volume = models.CharField(max_length=20, choices=VOLUME_CHOICES,
                              default='Маленькая: <1 m^3', verbose_name="Площадь", null=True)
    price = models.IntegerField(verbose_name='Цена за 1 м^3', null=True)

    location = models.CharField(
        max_length=150, verbose_name="Адрес", null=True)
    available_from = models.DateTimeField(verbose_name="Свободен с ")
    available_till = models.DateTimeField(verbose_name="Свободен до")

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'backend'


class StorageUser(models.Model):

    ROLE_CHOICES = [
        ('customer', "Клиент"),
        ('staff', "Работник"),
    ]

    tg_id = models.CharField(max_length=60, unique=True,
                             verbose_name="Телеграм id", null=True)
    property = models.ManyToManyField(StorageBox, related_name="owners")

    name = models.CharField(max_length=50, null=True, verbose_name="Имя")
    number = models.IntegerField(verbose_name='Номер', null=True)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='customer', verbose_name="Роль", null=True)

    def __str__(self):
        return f'{self.name} ({self.get_role_display()})'


class Order(models.Model):

    STATUS_CHOICES = [
        ('Обработывается', "Обработывается"),
        ('На складе', "На складе"),
        ('Завершен', "Завершен"),
        ('Задержка', "Задержка"),
    ]

    user = models.ForeignKey(StorageUser, on_delete=models.CASCADE,
                             related_name="orders", verbose_name="Пользователь")
    box = models.ForeignKey(StorageBox, on_delete=models.CASCADE,
                            related_name="orders", verbose_name="Склад", null=True)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='Обработывается', verbose_name="Статус", null=True)
    items_description = models.TextField(
        verbose_name="Описание вещей", null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Исправлено")

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class Delivery(models.Model):
    DELIVERY_CHOICES = [
        ('delivery_курьером', 'Заказ курьер'),
        ('delivery_самовывозом', 'Самовывоз')

    ]
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="delivery", verbose_name="Заказ")

    pickup_address = models.CharField(
        max_length=255, verbose_name="Адрес получения")
    contact_number = models.CharField(
        max_length=20, verbose_name="Контактный номер")
    scheduled_at = models.DateTimeField(
        verbose_name="Назначенная дата")
    delivery_method = models.CharField(max_length=30, choices=DELIVERY_CHOICES,
                                       default='delivery_самовывозом', verbose_name="Метод получения", null=True)

    completed = models.BooleanField(
        default=False, verbose_name="Завершено", null=True)

    def __str__(self):
        return f"Delivery for Order #{self.order.id}"


class Promotion(models.Model):
    valid_from = models.DateTimeField(verbose_name="Действует с ")
    valid_till = models.DateTimeField(verbose_name="Действует до ")

    def __str__(self):
        return self.code
