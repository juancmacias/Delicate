"""
Serializers for invoice models and API operations.
"""

from rest_framework import serializers
from .models import Invoice, InvoiceItem
from decimal import Decimal
from delicate_apps.type.serializers import TypeSerializer
from delicate_apps.users.serializers import UserSerializer
from delicate_apps.company.serializers import CompanySerializer

class InvoiceItemSerializer(serializers.ModelSerializer):
    """
    Serializer for invoice items with calculated fields for pricing.
    """
    product_name = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    formatted_price = serializers.SerializerMethodField()
    formatted_subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = InvoiceItem
        fields = [
            'id', 'invoice', 'product', 'quantity', 'price',
            'product_name', 'subtotal', 'formatted_price', 'formatted_subtotal'
        ]
    
    def get_product_name(self, obj):
        """Get product name or None if product is missing."""
        return obj.product.name if obj.product else None
    
    def get_subtotal(self, obj):
        """Calculate subtotal for this item."""
        return obj.get_total()
    
    def get_formatted_price(self, obj):
        """Format unit price with currency symbol."""
        return f"{round(Decimal(str(obj.price)), 2):.2f} €"
    
    def get_formatted_subtotal(self, obj):
        """Format subtotal with currency symbol."""
        return f"{obj.get_total():.2f} €"

class InvoiceSerializer(serializers.ModelSerializer):
    """
    Basic serializer for invoice list views.
    Includes calculated totals but not detailed relationships.
    """
    total = serializers.SerializerMethodField()
    formatted_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'date', 'payment_form', 'neto', 'fk_type', 
            'fk_user', 'fk_company', 'total', 'formatted_total'
        ]
    
    def get_total(self, obj):
        """Get invoice total including IVA."""
        return obj.get_total()
    
    def get_formatted_total(self, obj):
        """Format total with currency symbol."""
        return f"{obj.get_total():.2f} €"

class InvoiceDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for invoice detail views.
    Includes related objects and invoice items.
    """
    # Nested serializers for related models
    fk_type = TypeSerializer(read_only=True)
    fk_user = UserSerializer(read_only=True)
    fk_company = CompanySerializer(read_only=True)
    items = InvoiceItemSerializer(many=True, read_only=True)

    # Calculated fields
    total = serializers.SerializerMethodField()
    formatted_total = serializers.SerializerMethodField()
    iva_amount = serializers.SerializerMethodField()
    formatted_iva = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'date', 'payment_form', 'neto', 'fk_type', 
            'fk_user', 'fk_company', 'items', 'total', 
            'formatted_total', 'iva_amount', 'formatted_iva'
        ]
    
    def get_total(self, obj):
        """Get invoice total including IVA."""
        return obj.get_total()
    
    def get_formatted_total(self, obj):
        """Format total with currency symbol."""
        return f"{obj.get_total():.2f} €"
    
    def get_iva_amount(self, obj):
        """Get total IVA amount for the invoice."""
        return obj.get_iva_amount()
    
    def get_formatted_iva(self, obj):
        """Format IVA amount with currency symbol."""
        return f"{obj.get_iva_amount():.2f} €"