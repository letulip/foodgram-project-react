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

    is_in_shop_list = BooleanFilter(method='get_is_in_shop_list')
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorite = BooleanFilter(method='get_is_favorite')

    class Meta():
        fields = (
            'author',
            'tags',
            'is_favorite',
            'is_in_shop_list',
        )
        model = Recipe

    def get_is_in_shop_list(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(shop_list__user=self.request.user)

    def get_is_favorite(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(favorites__user=self.request.user)
