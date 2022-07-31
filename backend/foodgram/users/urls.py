from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UsersViewSet, UserKeyView, UserKeyDeleteView

app_name = 'users'

router = routers.DefaultRouter()
router.register(
    r'users',
    UsersViewSet,
    basename='UsersViewSet'
)


# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # path(
    #     'users/',
    #     # UsersAuthView todo
    #     name='register_user'
    # ),
    path(
        'auth/token/login/',
        UserKeyView.as_view(),
        # TokenObtainPairView.as_view(),
        name='get_token'
    ),
    path(
        'auth/token/logout/',
        UserKeyDeleteView.as_view(),
        name='delete_token'
    ),
    path('', include(router.urls)),
]
