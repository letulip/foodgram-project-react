from rest_framework.serializers import ModelSerializer

from .models import User


class UsersSerializer(ModelSerializer):

    class Meta():
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name'
        )
        model = User
