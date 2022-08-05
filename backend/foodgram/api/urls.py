from django.urls import include, path
from rest_framework import routers

from .views import TagsViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(
    r'tags',
    TagsViewSet,
    basename='TagsViewSet'
)
# router.register(
#     r'ingredients',
#     IngredientsViewSet,
#     basename='IngredientsViewSet'
# )
# router.register(
#     r'recipes',
#     RecipesViewSet,
#     basename='RecipesViewSet'
# )

urlpatterns = [
    # path(
    #     'auth/token/logout/',
    #     UserKeyDeleteView.as_view(),
    #     name='delete_token'
    # ),
    path('', include(router.urls)),
]
