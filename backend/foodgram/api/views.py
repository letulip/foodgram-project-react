# from django.http import HttpRequest
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientsSerializer, RecipesSerializer, RecipeEditSerializer
from .pagination import PageNumberPagination
from .permissions import IsOwnerOrReadOnly


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method not in ('POST', 'PATCH'):
            return RecipesSerializer
        return RecipeEditSerializer

    # def get_serializer_context(self):
        # return super().get_serializer_context()