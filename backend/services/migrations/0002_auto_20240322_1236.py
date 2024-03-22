# Generated by Django 3.1.4 on 2024-03-22 07:36

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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.category', verbose_name='Категория сервиса'),
        ),
        migrations.AddField(
            model_name='service',
            name='subscription_terms',
            field=models.ManyToManyField(related_name='services', through='services.TermsInService', to='services.Terms', verbose_name='Условия подписки'),
        ),
    ]
