# Generated by Django 3.1.4 on 2024-03-22 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20240322_1315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='subscription_terms',
            new_name='service_terms',
        ),
        migrations.AlterField(
            model_name='termsinservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services_list', to='services.service', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='termsinservice',
            name='terms',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terms_list', to='services.terms', verbose_name='Рецепт'),
        ),
        migrations.CreateModel(
            name='CategoryInService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_services', to='services.terms', verbose_name='Рецепт')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_categories', to='services.service', verbose_name='Ингредиент')),
            ],
        ),
    ]