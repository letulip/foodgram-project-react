import json

from django.core.management.base import BaseCommand

from api.models import Ingredient


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

        file_tags = json.load(open('../../data/tags.json'))
        count = 0

        for row in file_tags:
            Ingredient.objects.create(
                id=count,
                name=row['name'],
                color=row['color'],
                slug=row['slug'],
            )
            count += 1

        print('Data inserted Successfully')
