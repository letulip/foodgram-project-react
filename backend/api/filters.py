from django_filters.rest_framework import (AllValuesMultipleFilter,
                                           BooleanFilter, ModelMultipleChoiceFilter, FilterSet)
from rest_framework.filters import SearchFilter

from .models import Recipe, Tag


class IngredsFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(FilterSet):
    """
    Фильтры сортировки рецептов по тегам, избранному и корзине.
    """

    # tags = ModelMultipleChoiceFilter(
    #     field_name='tags__slug',
    #     queryset=Tag.objects.all(),
    #     to_field_name='slug',
    # )
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_in_shop_list = BooleanFilter(method='get_is_in_shop_list')
    is_favorited = BooleanFilter(method='get_is_favorited')

    class Meta():
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shop_list',
        )
        model = Recipe

    def get_is_in_shop_list(self, queryset, name, value):
        if not value:
            return Recipe.objects.all()
        return queryset.filter(shop_list__user=self.request.user)

    def get_is_favorited(self, queryset, name, value):
        if not value:
            return Recipe.objects.all()
        return queryset.filter(favorites__user=self.request.user)
