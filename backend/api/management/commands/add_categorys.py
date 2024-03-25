import csv

from django.core.management.base import BaseCommand

from PAY2U.settings import CSV_FILES_DIR
from services.models import Category


class Command(BaseCommand):
    """Команда для загрузки категорий в базу данных """

    help = 'Загрузка категорий в базу данных'

    def handle(self, *args, **kwargs):
        with open(
                f'{CSV_FILES_DIR}/categorys.csv', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            next(reader)
            categorys = [
                Category(
                    name=row[0],
                    text=row[1],
                )
                for row in reader
            ]
            Category.objects.bulk_create(categorys)
        print('Категории в базу данных загружены')
        print('ADD', Category.objects.count(), 'Category')
