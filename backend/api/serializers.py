from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField,
                                        SlugRelatedField, ValidationError)
from shoplist.models import ShopList
from users.serializers import UserSelfSerializer

from .models import Favorite, Ingredient, IngredientsAmount, Recipe, Tag


class TagSerializer(ModelSerializer):
    """
    Сериализатор отображения тегов.
    """

    class Meta:
        fields = (
            'name',
            'color',
            'slug',
        )
        model = Tag
        lookup_field = 'id'
        extra_kwargs = {
            'url': {
                'lookup_field': 'id'
            }
        }


class IngredientsSerializer(ModelSerializer):
    """
    Сериализатор отображения ингредиентов.
    """

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        model = Ingredient


class IngredientsAmountSerializer(ModelSerializer):
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

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )
        model = IngredientsAmount


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

    class Meta:
        fields = (
            'id',
            'amount',
        )
        model = IngredientsAmount


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
    is_favorited = SerializerMethodField(
        read_only=True,
    )

    class Meta:
        fields = (
            'id',
            'author',
            'name',
            'image',
            'ingredients',
            'text',
            'cooking_time',
            'tags',
            'is_favorited',
            'is_in_shop_list',
        )
        model = Recipe

    def get_ingredients(self, obj):
        recipe = obj
        queryset = recipe.ingreds_list.all()
        return IngredientsAmountSerializer(
            queryset,
            many=True,
        ).data

    def get_is_in_shop_list(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return ShopList.objects.filter(
                user=user,
                recipe=obj,
            ).exists()
        return False

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Favorite.objects.filter(
                user=user,
                recipe=obj,
            ).exists()
        return False


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

    class Meta:
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
            IngredientsAmount.objects.create(
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
        if not tags:
            raise ValidationError({
                'tags': 'At least 1 tag is required'
            })
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
        IngredientsAmount.objects.filter(recipe=recipe).delete()
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


class FavoriteSerializer(ModelSerializer):
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

    class Meta:
        fields = (
            'user',
            'recipe',
        )
        model = Favorite
