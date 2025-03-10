from rest_framework import serializers
from .models import Invoice, InvoiceItem
from decimal import Decimal
from delicate_apps.type.serializers import TypeSerializer
from delicate_apps.users.serializers import UserSerializer
from delicate_apps.company.serializers import CompanySerializer

class InvoiceItemSerializer(serializers.ModelSerializer):
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
        return obj.product.name if obj.product else None
    
    def get_subtotal(self, obj):
        return obj.get_total()
    
    def get_formatted_price(self, obj):
        return f"{round(Decimal(str(obj.price)), 2):.2f} €"
    
    def get_formatted_subtotal(self, obj):
        return f"{obj.get_total():.2f} €"

class InvoiceSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    formatted_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'date', 'payment_form', 'neto', 'fk_type', 
            'fk_user', 'fk_company', 'total', 'formatted_total'
        ]
    
    def get_total(self, obj):
        return obj.get_total()
    
    def get_formatted_total(self, obj):
        return f"{obj.get_total():.2f} €"

class InvoiceDetailSerializer(serializers.ModelSerializer):
    fk_type = TypeSerializer(read_only=True)
    fk_user = UserSerializer(read_only=True)
    fk_company = CompanySerializer(read_only=True)
    items = InvoiceItemSerializer(many=True, read_only=True)
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
        return obj.get_total()
    
    def get_formatted_total(self, obj):
        return f"{obj.get_total():.2f} €"
    
    def get_iva_amount(self, obj):
        return obj.get_iva_amount()
    
    def get_formatted_iva(self, obj):
        return f"{obj.get_iva_amount():.2f} €"