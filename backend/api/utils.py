from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from .models import Recipe


def create_response(recipe_id, serializer, user, error_message):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    serializer.is_valid(raise_exception=True)
    try:
        serializer.save(user=user, recipe=recipe)
    except IntegrityError:
        message = {
            'unique_together': error_message,
        }
        return Response(
            data=message,
            status=HTTP_400_BAD_REQUEST,
        )
    return Response(
        serializer.data,
        status=HTTP_201_CREATED,
    )


def delete_response(recipe_id, user, instance):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    instance.objects.filter(
        user=user,
        recipe=recipe
    ).delete()
    return Response(
        status=HTTP_204_NO_CONTENT,
    )
