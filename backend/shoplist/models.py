from api.models import Recipe
from django.db import models
from users.models import User


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
        unique_together = [
            ('user', 'recipe',)
        ]

    def __str__(self) -> str:
        full_name = f'{self.user}, {self.recipe}'
        return full_name
