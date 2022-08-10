from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from .serializers import ShopListSerializer
from .models import ShopList
from api.models import Recipe


class ShopListViewSet(ModelViewSet):
    queryset = ShopList.objects.all()
    serializer_class = ShopListSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        ShopList.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        return Response(
            status=HTTP_204_NO_CONTENT,
        )
