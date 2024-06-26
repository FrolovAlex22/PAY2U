# Generated by Django 4.1.2 on 2024-04-06 12:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=19, verbose_name='Номер карты')),
                ('balance', models.PositiveIntegerField(default=5000, verbose_name='Баланс')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активная карта')),
            ],
            options={
                'verbose_name': 'Банковская карта',
                'verbose_name_plural': 'Банковские карты',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Название категории не соответствует, можно использовать только буквы, цифры и нижнее подчеркивания.', regex='^[\\w.@+-]+$')], verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Comparison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Сравнение',
                'verbose_name_plural': 'Сравнении',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Название сервиса не соответствует, можно использовать только буквы, цифры и нижнее подчеркивания.', regex='^[\\w.@+-]+$')], verbose_name='Название сервиса')),
                ('image', models.ImageField(upload_to='services/images/', verbose_name='Логотип сервиса')),
                ('text', models.TextField(verbose_name='Описание сервиса')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Лучшее предложение')),
            ],
            options={
                'verbose_name': 'Сервис',
                'verbose_name_plural': 'Сервисы',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('subscription_type', models.CharField(choices=[('free', 'Бесплатная подписка'), ('paid', 'Платная подписка'), ('trial', 'Пробная подписка')], default='free', max_length=100, verbose_name='Тип подписки')),
                ('duration', models.CharField(choices=[('one_month', 'Один месяц'), ('three_months', 'Три месяца'), ('six_months', 'Шесть месяцев'), ('one_year', 'Один год')], max_length=150, verbose_name='Продолжительность')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('cashback', models.PositiveIntegerField(verbose_name='Кэшбэк')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription_terms', to='services.service', verbose_name='Связанный сервис')),
            ],
            options={
                'verbose_name': 'Условия подписки',
                'verbose_name_plural': 'Условия подписок',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Дата начала подписки')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания подписки')),
                ('bank_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscriptions', to='services.bankcard', verbose_name='Банковская карта')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='services.service', verbose_name='Сервис')),
                ('terms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='services.terms', verbose_name='Тариф')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
                'ordering': ('id',),
            },
        ),
    ]
