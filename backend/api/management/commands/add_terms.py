import csv

from django.core.management.base import BaseCommand

from PAY2U.settings import CSV_FILES_DIR
from services.models import Terms


class Command(BaseCommand):
    """Команда для загрузки условий в базу данных """

    help = 'Загрузка условий в базу данных'

    def handle(self, *args, **kwargs):
        with open(
                f'{CSV_FILES_DIR}/terms.csv', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            next(reader)
            ingredients = [
                Terms(
                    name=row[0],
                    duration=row[1],
                    price=row[2],
                    cashback=row[3]
                )
                for row in reader
            ]
            Terms.objects.bulk_create(ingredients)
        print('Условия в базу данных загружены')
        print('ADD', Terms.objects.count(), 'Terms')
