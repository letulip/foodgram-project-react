from rest_framework.serializers import ModelSerializer
from .models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        fields = (
            'name',
            'color',
            'slug',
        )
        model = Tag
        lookup_field = 'id'
