from django.urls import include, path
from rest_framework import routers

from .views import ShopListViewSet

app_name = 'shoplist'

router = routers.DefaultRouter()
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_list',
    ShopListViewSet,
    basename='ShopListViewSet'
)

urlpatterns = [
    path('', include(router.urls)),
]