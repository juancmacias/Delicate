from rest_framework import serializers
from .models import StoreProduct
from delicate_apps.type.serializers import TypeSerializer
from delicate_apps.company.serializers import CompanySerializer

class StoreProductSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    stock_status = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = StoreProduct
        fields = '__all__'
    
    # Calculate and return the total price with IVA included
    def get_total_price(self, obj):
        return obj.get_total_price()
    
    def get_stock_status(self, obj):
        if obj.stock <= 0:
            return "Agotado"
        elif obj.stock < 5:
            return f"¡Últimas {obj.stock} unidades!"
        return f"Disponible ({obj.stock} en stock)"
 
class StoreProductDetailSerializer(serializers.ModelSerializer):
    fk_type = TypeSerializer(read_only=True)
    fk_company = CompanySerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    stock_status = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = StoreProduct
        fields = '__all__'
        extraa_kwargs = {
            'image': {'required': False}
        }
    
    # Calculate and return the total price with IVA included
    def get_total_price(self, obj):
        return obj.get_total_price()

    # Calculate and return the stock status
    def get_stock_status(self, obj):
        if obj.stock <= 0:
            return "Agotado"
        elif obj.stock < 5:
            return f"¡Últimas {obj.stock} unidades!"
        return f"Disponible ({obj.stock} en stock)"

    # Get the image URL
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None