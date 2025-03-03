from rest_framework import serializers
from .models import BasketTemp
from delicate_apps.users.serializers import UserSerializer
from delicate_apps.store.serializers import ProductSerializer

class BasketTempSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = BasketTemp
        fields = '__all__'

    def get_total(self, obj):
        return obj.get_total()

class BasketTempDetailSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    product_id = StoreProductSerializer(read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = BasketTemp
        fields = '__all__'

        def get_total(self, obj):
        return obj.get_total()