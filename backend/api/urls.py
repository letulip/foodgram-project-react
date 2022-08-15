from django.urls import include, path
from rest_framework import routers

from .views import (DownloadShopListView, FavoriteViewSet, IngredientsViewSet,
                    RecipesViewSet, ShopListViewSet, TagsViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register(
    'tags',
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
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='RecipeFavoriteViewSet'
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShopListViewSet,
    basename='ShopListViewSet'
)

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        DownloadShopListView.as_view(),
        name='download_shop_list'
    ),
    path('', include(router.urls)),
]
