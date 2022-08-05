from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, SlugRelatedField, SerializerMethodField
from .models import Tag, Ingredient, Recipe, IngredsAmount


class TagSerializer(ModelSerializer):
    class Meta():
        fields = (
            'name',
            'color',
            'slug',
        )
        model = Tag
        lookup_field = 'id'


class IngredientsSerializer(ModelSerializer):
    
    class Meta():
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        model = Ingredient


class IngredsAmountSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(
        source='ingredient',
        read_only=True,
    )
    name = SlugRelatedField(
        slug_field='name',
        source='ingredient',
        read_only=True,
    )
    measurement_unit = SlugRelatedField(
        slug_field='measurement_unit',
        source='ingredient',
        read_only=True,
    )

    class Meta():
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipesSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    ingredients = SerializerMethodField()
    tags = TagSerializer(
        many=True,
        read_only=True,
    )

    class Meta():
        fields = (
            'id',
            'author',
            'name',
            'image',
            'ingredients',
            'text',
            'cooking_time',
            'tags',
        )

    def get_ingredients(self, obj):
        return IngredsAmountSerializer(
            queryset=obj.ingreds_list.all(),
            many=True,
        ).data


class RecipeImageSerializer(ModelSerializer):
    pass