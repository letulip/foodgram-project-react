from django.urls import include, path
from rest_framework import routers

from .views import UsersViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register(
    r'users',
    UsersViewSet,
    basename='UsersViewSet'
)

urlpatterns = [
    # path(
    #     'users/',
    #     # UsersAuthView todo
    #     name='register_user'
    # ),
    # path(
    #     'users/(?P<post_id>[0-9]+)/',
    #     # UserView todo
    #     name='user_view'
    # ),
    path('', include(router.urls)),
]
