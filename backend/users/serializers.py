from api.models import Recipe
from django.core.validators import RegexValidator
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        SerializerMethodField)

from .models import Subscriptions, User


class UsersSerializer(ModelSerializer):
    """
    Общий сериализатор пользователей.
    """

    class Meta():
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSelfSerializer(UsersSerializer):
    """
    Сериализатор просмотра личной страницы пользователя.
    """

    is_subscribed = SerializerMethodField(
        read_only=True,
    )
    username = CharField(
        max_length=150,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message="""This value may contain only letters,
                digits and @/./+/-/_ characters."""
            ),
            RegexValidator(
                regex=r'^\b(m|M)e\b',
                inverse_match=True,
                message="""Username Me registration not allowed."""
            )
        ],
    )
    email = EmailField(
        required=False,
        max_length=254
    )
    password = CharField(
        required=False,
        max_length=150
    )

    class Meta():
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscriptions.objects.filter(
            user=user,
            author=obj.id
        ).exists()


class SubscriptionsRecipeSerializer(ModelSerializer):
    """
    Сериализатор отображения рецептов в подписках.
    """

    class Meta():
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionsSerializer(UserSelfSerializer):
    """
    Сериализатор отображения подписок.
    """

    recipes = SerializerMethodField(read_only=True)
    recipes_count = SerializerMethodField(read_only=True)

    class Meta():
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        model = User

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return SubscriptionsRecipeSerializer(
            recipes,
            many=True
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
