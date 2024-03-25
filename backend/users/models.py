from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователей."""

    email = models.EmailField(
        max_length=254,
        unique=True,
        db_index=True,
        verbose_name='Имейл'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя не соответствует, '
                        'можно использовать только буквы, '
                        'цифры и нижнее подчеркивания.'
            )
        ],
        verbose_name='Имя пользователя'
    )
    phone_number = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Телефонный номер должен быть формата: +"999999999".'
            )
        ],
        max_length=17,
        verbose_name='Телефонный номер',
    )
    balance = models.PositiveIntegerField(
        default=10000,
        verbose_name='Баланс'
    )
    credit_cart = ...

    comparison_sheet = ...
    

    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
