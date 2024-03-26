from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель для описания категории"""
    name = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Название категории не соответствует, '
                        'можно использовать только буквы, '
                        'цифры и нижнее подчеркивания.'
            )
        ],
        verbose_name='Название категории'
    )

    class Meta:
        """Мета-параметры модели"""

        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Метод строкового представления модели."""

        return self.name


class Service(models.Model):
    """Модель для описания сервиса"""

    name = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Название сервиса не соответствует, '
                        'можно использовать только буквы, '
                        'цифры и нижнее подчеркивания.'
            )
        ],
        verbose_name='Название сервиса'
    )
    category = models.ForeignKey(
        Category,
        related_name='services',
        on_delete=models.CASCADE,
        verbose_name='Категория сервиса',
    )
    image = models.ImageField(
        upload_to='services/images/',
        verbose_name='Логотип сервиса',
    )
    text = models.TextField(
        verbose_name='Описание сервиса'
    )
    is_featured = models.BooleanField(default=False, verbose_name='Лучшее предложение')

    class Meta:
        """Мета-параметры модели"""

        ordering = ('id',)
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        """Метод строкового представления модели."""

        return self.name


class Terms(models.Model):
    """Модель для описания условия подписки"""

    DURATION_CHOICES = [
        ("one_month", "Один месяц"),
        ("three_months", "Три месяца"),
        ("six_months", "Шесть месяцев"),
        ("one_year", "Один год"),
    ]

    SUB_TYPE = [
        ('free', 'Бесплатная подписка'),
        ('paid', 'Платная подписка'),
        ('trial', 'Пробная подписка'),
    ]

    name = models.CharField(
        max_length=150,
    )
    subscription_type = models.CharField(
        max_length=100,
        choices=SUB_TYPE,
        default='free',
        verbose_name='Тип подписки',
    )
    duration = models.CharField(
        max_length=150,
        choices=DURATION_CHOICES,
        verbose_name='Продолжительность',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена'
    )
    cashback = models.PositiveIntegerField(
        verbose_name='Кэшбэк'
    )
    service = models.ForeignKey(
        Service,
        related_name='subscription_terms',
        on_delete=models.CASCADE,
        verbose_name='Связанный сервис',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Условия подписки'
        verbose_name_plural = 'Условия подписок'

    def __str__(self):
        return f'{self.name}'


class BankCard(models.Model):
    """Модель банковской карты для демонстрационных целей."""
    card_number = models.CharField(max_length=19, verbose_name='Номер карты')  # 16 цифр + 3 пробела для форматирования
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bank_cards',
        verbose_name='Владелец карты',
    )
    balance = models.PositiveIntegerField(
        default=5000,
        verbose_name='Баланс'
    )
    is_active = models.BooleanField(default=False, verbose_name='Активная карта')

    class Meta:
        verbose_name = 'Банковская карта'
        verbose_name_plural = 'Банковские карты'

    def __str__(self):
        return f'Карта {self.card_number[-4:]} пользователя {self.user.username}'


class Subscription(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Сервис',
    )
    terms = models.ForeignKey(
        Terms,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Тариф',
    )
    start_date = models.DateTimeField(
        blank=True,
        default=timezone.now,
        verbose_name='Дата начала подписки'
    )
    end_date = models.DateTimeField(
        blank=True,
        verbose_name='Дата окончания подписки'
    )
    bank_card = models.ForeignKey(
        BankCard,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscriptions',
        verbose_name='Банковская карта',
    )

    class Meta:
        unique_together = ('user', 'service', 'terms')
        ordering = ('id',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.service}'
