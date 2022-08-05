from django.db import models
from django.core.validators import RegexValidator

from users.models import User

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(
        max_length=150,
    )
    measurement_unit = models.CharField(
        max_length=20,
    )
    quantity = models.FloatField(
        null=True
    )

class Tag(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='tag name',
        unique=True,
        null=False,
    )
    color = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^#([A-Fa-f\d]{6,8})',
                message="""This value may contain only letters and
                digits."""
            )
        ],
        default='#ffffff'
    )
    slug = models.SlugField(
        max_length=150,
        verbose_name='tug slug',
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )
    name = models.CharField(
        max_length=200,
    )
    image = models.ImageField(
        upload_to='recipes/',
    )
    tags = models.ManyToManyField(Tag)
    text = models.TextField()
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient)
