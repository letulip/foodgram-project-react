from django.core.validators import RegexValidator
from rest_framework.serializers import CharField, EmailField, ModelSerializer, SlugRelatedField

from .models import User, Subscriptions


class UsersSerializer(ModelSerializer):

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
    # role = CharField(read_only=True)
    password = CharField(
        required=False,
        max_length=150
    )


class SubscriptionsSerializer(ModelSerializer):
    user = SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
    )
    author = SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        default=UserSelfSerializer(),
    )

    class Meta():
        fields = (
            'user',
            'author',
        )
        model = Subscriptions


class SubscriptionsListSerializer(ModelSerializer):
    username = SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
    )
    author = SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        default=UserSelfSerializer(),
    )

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
        model = Subscriptions
