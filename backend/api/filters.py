from django_filters.rest_framework import (AllValuesMultipleFilter,
                                           BooleanFilter, FilterSet)
from rest_framework.filters import SearchFilter

from .models import Recipe


class IngredsFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(FilterSet):
    """
    Фильтры сортировки рецептов по тегам, избранному и корзине.
    """

    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_in_shopping_cart = BooleanFilter(method='get_is_in_shopping_cart')
    is_favorited = BooleanFilter(method='get_is_favorited')

    class Meta:
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        )
        model = Recipe

    def get_is_in_shopping_cart(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(shop_list__user=self.request.user)

    def get_is_favorited(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(favorites__user=self.request.user)
