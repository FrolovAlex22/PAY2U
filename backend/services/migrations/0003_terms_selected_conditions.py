# Generated by Django 4.1.2 on 2024-03-28 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_alter_subscription_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='terms',
            name='selected_conditions',
            field=models.BooleanField(default=False, verbose_name='выбранный сервис'),
        ),
    ]
