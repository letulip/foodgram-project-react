from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredsFilter, RecipesFilter
from .models import Favorite, Ingredient, Recipe, Tag
from .pagination import CustomPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (FavoriteSerializer, IngredientsSerializer,
                          RecipeEditSerializer, RecipesSerializer,
                          TagSerializer)


class TagsViewSet(ReadOnlyModelViewSet):
    """
    Отображение списка тегов.
    Доступно всем пользователям.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


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
        return user.Favorite.all()

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            serializer.save(user=request.user, recipe=recipe)
        except IntegrityError:
            message = {
                'unique_together': 'Recipe already in your Favorite',
            }
            return Response(
                data=message,
                status=HTTP_400_BAD_REQUEST,
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
            headers=headers
        )

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        Favorite.objects.filter(
            user=user,
            recipe=recipe,
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)
