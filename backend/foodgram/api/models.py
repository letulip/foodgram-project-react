from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='ingredient name'
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='measurement unit'
    )

    def __str__(self) -> str:
        full_name = f'{self.name}, {self.measurement_unit}'
        return full_name


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
        related_name='recipes',
        verbose_name='Recipe Author',
    )
    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Recipe Name'
    )
    image = models.ImageField(
        upload_to='recipes/',
    )
    text = models.TextField(
        verbose_name='Recipe Description'
    )
    cooking_time = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, 'Cooking time must be 1 at least'),
        ],
        verbose_name='Cooking time in minutes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
        through='IngredsAmount',
        verbose_name='Recipe Ingredients',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Recipe Tag',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Publication Date',
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.name


class IngredsAmount(models.Model):
    ingedient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ingredient',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingreds_list',
        verbose_name='Recipe ingreds list',
    )
    amount = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, 'Ingredient amount must be 1 at least'),
        ],
        verbose_name='Amount of ingredients',
    )

    def __str__(self) -> str:
        full_name = f'{self.ingedient} для рецепта {self.recipe}'
        return full_name
