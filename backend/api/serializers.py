from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField,
                                        SlugRelatedField)
from shoplist.models import ShopList
from users.serializers import UserSelfSerializer

from .models import Favorites, Ingredient, IngredsAmount, Recipe, Tag


class TagSerializer(ModelSerializer):
    """
    Сериализатор отображения тегов.
    """

    class Meta():
        fields = (
            'name',
            'color',
            'slug',
        )
        model = Tag
        lookup_field = 'id'


class IngredientsSerializer(ModelSerializer):
    """
    Сериализатор отображения ингредиентов.
    """

    class Meta():
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        model = Ingredient


class IngredsAmountSerializer(ModelSerializer):
    """
    Сериализатор отображения ингредиентов с количеством.
    """

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
        model = IngredsAmount


class AddIngredAmountSerializer(ModelSerializer):
    """
    Сериализатор добавления ингредиента с количеством.
    """

    id = IntegerField(
        write_only=True,
    )
    amount = IntegerField(
        write_only=True,
    )

    class Meta():
        fields = (
            'id',
            'amount',
        )
        model = IngredsAmount


class RecipesSerializer(ModelSerializer):
    """
    Сериализатор отображения рецепта.
    """

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    ingredients = SerializerMethodField()
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    is_in_shop_list = SerializerMethodField(
        read_only=True,
    )
    is_favorite = SerializerMethodField(
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
        model = Recipe

    def get_ingredients(self, obj):
        recipe = obj
        queryset = recipe.ingreds_list.all()
        return IngredsAmountSerializer(
            queryset,
            many=True,
        ).data

    def is_in_shop_list(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return False
        return ShopList.objects.filter(
            user=user,
            recipe=obj,
        ).exists()

    def is_favorite(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return False
        return Favorites.objects.filter(
            user=user,
            recipe=obj,
        ).exists()


class RecipeEditSerializer(ModelSerializer):
    """
    Сериализатор редактирования рецепта.
    """

    image = Base64ImageField(
        use_url=True,
    )
    author = UserSelfSerializer(
        read_only=True,
    )
    ingredients = AddIngredAmountSerializer(
        many=True,
    )
    tags = PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    cooking_time = IntegerField()

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
        model = Recipe

    def create_ingreds(self, recipe, ingredients):
        for item in ingredients:
            ingredient = get_object_or_404(Ingredient, id=item['id'])
            IngredsAmount.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=item['amount']
            )

    # use atomic to roll back db transaction due to error
    @atomic
    def create(self, validated_data):
        user = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=user,
            **validated_data
        )
        self.create_ingreds(recipe, ingredients)
        recipe.tags.set(tags)
        recipe.save()
        return recipe

    @atomic
    def update(self, recipe, validated_data):
        print(validated_data)
        IngredsAmount.objects.filter(recipe=recipe).delete()
        ingredients = validated_data.pop('ingredients')
        self.create_ingreds(recipe, ingredients)
        tags = validated_data.pop('tags')
        recipe.tags.set(tags)
        recipe.name = validated_data.pop('name')
        recipe.text = validated_data.pop('text')
        recipe.cooking_time = validated_data.pop('cooking_time')
        recipe.image = validated_data.pop('image')
        recipe.save()
        return recipe


class FavoritesSerializer(ModelSerializer):
    """
    Сериализатор отображения избранного.
    """

    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    recipe = SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta():
        fields = (
            'user',
            'recipe',
        )
        model = Favorites