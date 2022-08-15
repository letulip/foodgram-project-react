from django.urls import include, path
from rest_framework import routers

from .views import (SubscribeViewSet, SubscriptionViewSet, UserKeyDeleteView,
                    UserKeyView, UsersViewSet)

app_name = 'users'

router = routers.DefaultRouter()
router.register(
    r'users/subscriptions',
    SubscriptionViewSet,
    basename='SubscriptionViewSet'
)
router.register(
    r'users',
    UsersViewSet,
    basename='UsersViewSet'
)
router.register(
    r'users/(?P<author_id>\d+)/subscribe',
    SubscribeViewSet,
    basename='SubscribeViewSet'
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
