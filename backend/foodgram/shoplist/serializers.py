from rest_framework.serializers import ModelSerializer
from users.serializers import SubscriptionsRecipeSerializer
from .models import ShopList

class ShopListSerializer(ModelSerializer):

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
