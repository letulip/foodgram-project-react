from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from .models import Recipe


class IngredsFilter(SearchFilter):
    search_param = 'name'

class RecipesFilter(FilterSet):
    """
    Фильтры сортировки рецептов по тегам, избранному и корзине.
    """

    is_in_shop_list = filters.BooleanFilter(method='is_in_shop_list')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorite = filters.BooleanFilter(method='is_favorite')

    class Meta():
        fields = (
            'author',
            'tags',
            'is_favorite',
            'is_in_shop_list',
        )
        model = Recipe

    def is_in_shop_list(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(shop_list__user=self.request.user)

    def is_favorite(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(favorites__user=self.request.user)
