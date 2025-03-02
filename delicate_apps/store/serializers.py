from rest_framework import serializers
from .models import StoreProduct
from delicate_apps.type.serializers import TypeSerializer
from delicate_apps.company.serializers import CompanySerializer

class StoreProductSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = StoreProduct
        fields = '__all__'
    
    # Calculate and return the total price with IVA included
    def get_total_price(self, obj):
        return obj.get_total_price()
 
class StoreProductDetailSerializer(serializers.ModelSerializer):
    fk_type = TypeSerializer(read_only=True)
    fk_company = CompanySerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = StoreProduct
        fields = '__all__'
    
    # Calculate and return the total price with IVA included
    def get_total_price(self, obj):
        return obj.get_total_price()