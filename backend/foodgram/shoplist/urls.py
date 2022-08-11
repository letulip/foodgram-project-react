from django.urls import include, path
from rest_framework import routers

from .views import ShopListViewSet, DownloadShopListView

app_name = 'shoplist'

router = routers.DefaultRouter()
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
