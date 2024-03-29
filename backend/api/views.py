from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredsFilter, RecipesFilter
from .models import (Favorite, Ingredient, IngredientsAmount, Recipe, ShopList,
                     Tag)
from .pagination import CustomPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (FavoriteSerializer, IngredientsSerializer,
                          RecipeEditSerializer, RecipesSerializer,
                          ShopListSerializer, TagSerializer)
from .utils import create_response, delete_response


class TagsViewSet(ReadOnlyModelViewSet):
    """
    Отображение списка тегов.
    Доступно всем пользователям.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    """
    Отображение списка ингредиентов.
    Доступно всем пользователям.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (IngredsFilter,)
    search_fields = ('^name',)


class RecipesViewSet(ModelViewSet):
    """
    Отображение рецепта.
    Просмотр доступен всем пользователям.
    Редактирование доступно только автору рецепта.
    """

    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.request.method not in ('POST', 'PATCH'):
            return RecipesSerializer
        return RecipeEditSerializer


class FavoriteViewSet(ModelViewSet):
    """
    Отображение и редактирование избранных рецептов.
    Доступно только аутентифицированным пользователям.
    """

    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return user.favorites.all()

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        error_message = 'Recipe already in your favorites'
        serializer = self.get_serializer(data=request.data)
        return create_response(
            recipe_id,
            serializer,
            request.user,
            error_message
        )

    def delete(self, request, recipe_id):
        return delete_response(recipe_id, request.user, Favorite)


class ShopListViewSet(ModelViewSet):
    """
    Создание и удаление ингредиентов списка покупок.
    Доступно только авторизованным пользователям.
    """

    serializer_class = ShopListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.shop_list.all()

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        error_message = 'Recipe already in your shopping list'
        serializer = self.get_serializer(data=request.data)
        return create_response(
            recipe_id,
            serializer,
            request.user,
            error_message
        )

    def delete(self, request, recipe_id):
        return delete_response(recipe_id, request.user, ShopList)


class DownloadShopListView(APIView):
    """
    Скачивание списка покупок.
    Доступно только авторизованным пользователям.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        shop_list = {}
        ingredients = IngredientsAmount.objects.filter(
            recipe__ingreds_to_buy__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(ingredient_total=Sum('amount'))
        for item in ingredients:
            amount = item['ingredient_total']
            name = item['ingredient__name']
            unit = item['ingredient__measurement_unit']
            shop_list[name] = {
                'amount': amount,
                'unit': unit,
            }
        out_string = 'Ваш список покупок:\n'
        for name, item in shop_list.items():
            out_string += f'- {name}: {item["amount"]} {item["unit"]}\n'
        response = HttpResponse(
            out_string,
            'Content-Type: text/plain',
        )
        response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
        return response
