from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField,
                                        SlugRelatedField, ValidationError)

from users.serializers import SubscriptionRecipeSerializer, UserSelfSerializer
from .models import (Favorite, Ingredient, IngredientsAmount, Recipe, ShopList,
                     Tag)


class TagSerializer(ModelSerializer):
    """
    Сериализатор отображения тегов.
    """

    class Meta:
        fields = (
            'id',
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

    author = UserSelfSerializer(
        read_only=True,
    )
    ingredients = IngredientsAmountSerializer(
        many=True,
        source='ingreds_list',
        read_only=True,
    )
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
        objs = [
            IngredientsAmount(
                ingredient=get_object_or_404(Ingredient, id=item['id']),
                recipe=recipe,
                amount=item['amount']
            )
            for item in ingredients
        ]
        IngredientsAmount.objects.bulk_create(objs)

    def validate(self, data):
        ingreds_list = []
        for item in data['ingredients']:
            if item['id'] in ingreds_list:
                raise ValidationError({
                    'ingredients': 'Ingredient should be unique'
                })
            ingreds_list.append(item['id'])
            if int(item['amount']) <= 0:
                raise ValidationError({
                    'amount': 'Ingredient amount should be positive'
                })

        tags = data['tags']
        if not tags:
            raise ValidationError({
                'tags': 'At least 1 tag is required'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError({
                    'tags': 'Tag should be unique'
                })
            tags_list.append(tag)

        if int(data['cooking_time']) <= 0:
            raise ValidationError({
                'cooking_time': 'Cooking time should be positive'
            })
        return data

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
        return recipe

    @atomic
    def update(self, recipe, validated_data):
        IngredientsAmount.objects.filter(recipe=recipe).delete()
        ingredients = validated_data.pop('ingredients')
        self.create_ingreds(recipe, ingredients)
        tags = validated_data.pop('tags')
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)


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


class ShopListSerializer(ModelSerializer):
    """
    Сериализатор для работы со списком покупок.
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
        model = ShopList

    def to_representation(self, instance):
        context = {
            'request': self.context.get('request')
        }
        return SubscriptionRecipeSerializer(
            instance=instance.recipe,
            context=context
        ).data
