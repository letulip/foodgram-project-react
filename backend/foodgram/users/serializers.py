from django.core.validators import RegexValidator
from rest_framework.serializers import CharField, EmailField, ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


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

# from django.views.decorators.csrf import csrf_protect

class UserKeySerializer(TokenObtainPairSerializer):
    # class Meta():
    #     fields = (
    #         'email',
    #         'password'
    #     )
    #     model = User
    #     extra_kwargs = {'password': {'write_only': True}}
    username_field = User.EMAIL_FIELD

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields[self.email_field] = CharField(required=True)
    #     # self.fields['password'].required = False
    #     self.fields[self.password_field] = CharField(required=True)

    # @csrf_protect
    def validate(self, attrs):
        # attrs.update({'password': ''})
        return super(UserKeySerializer, self).validate(attrs)
