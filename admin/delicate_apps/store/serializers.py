"""
Serializers for store product models and API operations.
"""

from rest_framework import serializers
from .models import StoreProduct
from delicate_apps.type.serializers import TypeSerializer
from delicate_apps.company.serializers import CompanySerializer
from django.conf import settings

class StoreProductSerializer(serializers.ModelSerializer):
    """
    Basic serializer for StoreProduct model.
    Includes calculated fields for price and stock status.
    """
    total_price = serializers.SerializerMethodField()
    stock_status = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = StoreProduct
        fields = '__all__'
    
    def get_total_price(self, obj):
        """Calculate total price with IVA included."""
        return obj.get_total_price()
    
    def get_stock_status(self, obj):
        """Generate user-friendly stock status message."""
        if obj.stock <= 0:
            return "Agotado"
        elif obj.stock < 5:
            return f"¡Últimas {obj.stock} unidades!"
        return f"Disponible ({obj.stock} en stock)"
 
class StoreProductDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for StoreProduct with expanded related objects.
    Used for product detail views with full information.
    """
    # Include full related objects rather than just IDs
    fk_type = TypeSerializer(read_only=True)
    fk_company = CompanySerializer(read_only=True)

    # Calculated fields
    total_price = serializers.SerializerMethodField()
    stock_status = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = StoreProduct
        fields = '__all__'
        extraa_kwargs = {
            'image': {'required': False}
        }
    
    def get_total_price(self, obj):
        """Calculate total price with IVA included."""
        return obj.get_total_price()

    def get_stock_status(self, obj):
        """Generate user-friendly stock status message."""
        if obj.stock <= 0:
            return "Agotado"
        elif obj.stock < 5:
            return f"¡Últimas {obj.stock} unidades!"
        return f"Disponible ({obj.stock} en stock)"

    def get_image_url(self, obj):
        """Get full image URL from Cloudinary."""
        if obj.image:
            return f"{os.getenv('CLOUDINARY_URL_PREFIX')}{obj.image}"
        return None