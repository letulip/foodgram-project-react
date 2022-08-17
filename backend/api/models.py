from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """
    Основная модель объекта ингредиента.
    """

    name = models.CharField(
        max_length=150,
        verbose_name='ingredient name'
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='measurement unit'
    )

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """
    Модель объекта тега.
    """

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
        unique=True,
        default='#ffffff'
    )
    slug = models.SlugField(
        max_length=150,
        verbose_name='tag slug',
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """
    Модель объекта рецепта.
    """

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
        related_name='recipes',
        through='IngredientsAmount',
        verbose_name='Recipe Ingredients',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
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


class IngredientsAmount(models.Model):
    """
    Модель объекта ингредиента с количеством.
    """

    ingredient = models.ForeignKey(
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

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'ingredient',
                    'recipe',
                ),
                name='unique ingredient amount',
            ),
        )

    def __str__(self) -> str:
        return f'{self.ingredient} для рецепта {self.recipe}'


class Favorite(models.Model):
    """
    Модель объекта избранного.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    add_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Favorite added date',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'user',
                    'recipe',
                ),
                name='unique_recipe_per_user',
            )
        ]

    def __str__(self) -> str:
        return f'{self.recipe} добавлен в избранное {self.user}'


class ShopList(models.Model):
    """
    Модель списка покупок.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_list',
        verbose_name='Shopping List',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingreds_to_buy',
        verbose_name='Ingreds to buy',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='List creation date',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'user',
                    'recipe',
                ),
                name='unique_recipe_per_user',
            )
        ]

    def __str__(self) -> str:
        return f'{self.user}, {self.recipe}'
