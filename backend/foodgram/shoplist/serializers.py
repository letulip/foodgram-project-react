from rest_framework.serializers import ModelSerializer, SlugRelatedField
from users.serializers import SubscriptionsRecipeSerializer
from .models import ShopList

class ShopListSerializer(ModelSerializer):
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
        model = ShopList

    def to_representation(self, instance):
        context = {
            'request': self.context.get('request')
        }
        return SubscriptionsRecipeSerializer(
            instance=instance.recipe,
            context=context
        ).data
