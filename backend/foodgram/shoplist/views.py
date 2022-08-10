from django.db import IntegrityError
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

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        print(request)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )
        try:
            serializer.save(user=request.user, recipe=recipe)
        except IntegrityError:
            message = {
                'unique_together': 'Recipe already in your shopping list',
            }
            return Response(
                data=message,
                status=HTTP_400_BAD_REQUEST,
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
            headers=headers
        )

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
