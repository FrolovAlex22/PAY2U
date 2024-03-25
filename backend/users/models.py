from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователей."""

    email = models.EmailField(
        max_length=254,
        unique=True,
        db_index=True,
        verbose_name="Email"
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
    first_name = models.CharField("Имя", max_length=255)
    last_name = models.CharField("Фамилия", max_length=255)
    phone_number = models.CharField( # обратить внимание на это поле
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Телефонный номер должен быть формата: +"999999999".'
            )
        ],
        max_length=17,
        verbose_name='Телефонный номер',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username", 'phone_number', "first_name", "last_name"]

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
