import json

from api.models import Ingredient
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Кастомная команда для заполнения базы данными ингредиентами.
    """

    help = 'Import Ingredients'

    def handle(self, *args, **options):

        file = json.load(open('../../data/ingredients.json'))
        count = 0

        for row in file:
            Ingredient.objects.create(
                id=count,
                name=row['name'],
                measurement_unit=row['measurement_unit'],
            )
            count += 1

        print('Data inserted Successfully')
