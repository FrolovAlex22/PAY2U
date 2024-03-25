# Generated by Django 4.1.2 on 2024-03-25 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.category', verbose_name='Категория сервиса'),
        ),
        migrations.AddField(
            model_name='bankcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_cards', to=settings.AUTH_USER_MODEL, verbose_name='Владелец карты'),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together={('user', 'service', 'terms')},
        ),
    ]