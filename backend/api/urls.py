from django.urls import include, path
from rest_framework import routers

from .views import (FavoriteViewSet, IngredientsViewSet, RecipesViewSet,
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
    r'recipes/(?P<recipe_id>\d+)/Favorite',
    FavoriteViewSet,
    basename='RecipeFavoriteViewSet'
)

urlpatterns = [
    path('', include(router.urls)),
]
