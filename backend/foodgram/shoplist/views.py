from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .serializers import ShopListSerializer
from .models import ShopList
from api.models import Recipe, IngredsAmount


class ShopListViewSet(ModelViewSet):
    """
    Создание и удаление ингредиентов списка покупок.
    Доступно только авторизованным пользователям.
    """
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


class DownloadShopListView(APIView):
    """
    Скачивание списка покупок.
    Доступно только авторизованным пользователям.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        shop_list = {}
        ingredients = IngredsAmount.objects.filter(
            recipe__ingreds_to_buy__user=request.user
        )
        for item in ingredients:
            amount = item.amount
            name = item.ingredient.name
            unit = item.ingredient.measurement_unit
            if name not in shop_list:
                shop_list[name] = {
                    'amount': amount,
                    'unit': unit,
                }
            else:
                shop_list[name]['amount'] += amount
        out_string = 'Ваш список покупок:\n'
        for name, item in shop_list.items():
            out_string += f'- {name}: {item["amount"]} {item["unit"]}\n'
        response = HttpResponse(
            out_string,
            'Content-Type: text/plain',
        )
        response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
        return response
