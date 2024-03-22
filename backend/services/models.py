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
    text = models.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Описание категории не соответствует, '
                        'можно использовать только буквы, '
                        'цифры и нижнее подчеркивания.'
            )
        ],
        verbose_name='Описание категории'
    )

    REQUIRED_FIELDS = [
        'name',
        'text',
    ]

    class Meta:
        """Мета-параметры модели"""

        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Метод строкового представления модели."""

        return self.name


class Terms(models.Model):
    """Модель для описания условия подписки"""
    name = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Название условия подписки не соответствует, '
                        'можно использовать только буквы, '
                        'цифры и нижнее подчеркивания.'
            )
        ],
    )
    duration = models.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Название условия подписки не соответствует, '
                        'можно использовать только буквы, '
                        'цифры и нижнее подчеркивания.'
            )
        ],
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена'
    )
    cashback = models.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Название условия подписки не соответствует, '
                        'можно использовать только буквы, '
                        'цифры и нижнее подчеркивания.'
            )
        ],
        verbose_name='Кэшбэк'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Условия подписки'
        verbose_name_plural = 'Условия подписок'

    def __str__(self):
        return f'{self.name}'


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
    category = models.ManyToManyField(
        Category,
        related_name='services',
        on_delete=models.CASCADE,
        verbose_name='Категория сервиса',
    )
    image = models.ImageField(
        upload_to='services/',
        blank=True,
        verbose_name='Логотип сервиса',
    )
    text = models.TextField(
        verbose_name='Описание сервиса'
    )
    service_terms = models.ManyToManyField(
        Terms,
        through='TermsInService',
        related_name='services',
        verbose_name='Условия подписки',
    )

    REQUIRED_FIELDS = [
        'name',
        'category',
        'image',
        'text',
        'subscription_terms'
    ]

    class Meta:
        """Мета-параметры модели"""

        ordering = ('id',)
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        """Метод строкового представления модели."""

        return self.name


class TermsInService(models.Model):
    terms = models.ForeignKey(
        Terms,
        on_delete=models.CASCADE,
        related_name='terms_list',
        verbose_name='Рецепт',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='services_list'
    )


class CategoryInService(models.Model):
    category = models.ForeignKey(
        Terms,
        on_delete=models.CASCADE,
        related_name='category_services',
        verbose_name='Рецепт',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='service_categories'
    )


class Subscription(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Подписчик',
    )
    servece = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Сервис',
    )
    terms = models.ForeignKey(
        Terms,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Условия',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.servece}'
