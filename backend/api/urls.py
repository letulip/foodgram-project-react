from django.urls import include, path
from rest_framework import routers

from .views import (FavoritesViewSet, IngredientsViewSet, RecipesViewSet,
                    TagsViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register(
    r'tags',
    TagsViewSet,
    basename='TagsViewSet'
)
router.register(
    r'ingredients',
    IngredientsViewSet,
    basename='IngredientsViewSet'
)
router.register(
    r'recipes',
    RecipesViewSet,
    basename='RecipesViewSet'
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorites',
    FavoritesViewSet,
    basename='RecipeFavoritesViewSet'
)

urlpatterns = [
    path('', include(router.urls)),
]
