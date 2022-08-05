from django.urls import include, path
from rest_framework import routers

from .views import UsersViewSet, UserKeyView, UserKeyDeleteView

app_name = 'users'

router = routers.DefaultRouter()
router.register(
    r'users',
    UsersViewSet,
    basename='UsersViewSet'
)

urlpatterns = [
    path(
        'auth/token/login/',
        UserKeyView.as_view(),
        name='get_token'
    ),
    path(
        'auth/token/logout/',
        UserKeyDeleteView.as_view(),
        name='delete_token'
    ),
    path('', include(router.urls)),
]
