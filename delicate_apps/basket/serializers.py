from rest_framework import serializers
from .models import BasketTemp
from delicate_apps.invoices.models import Invoice, InvoiceItem
from delicate_apps.store.models import StoreProduct

class BasketTempSerializer(serializers.ModelSerializer):
    # Inputs calculated fields
    total = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_stock = serializers.SerializerMethodField()

    class Meta:
        model = BasketTemp
        fields = [
            'id', 'user_id', 'product_id', 'cantidad', 'precio',
            'temp_date', 'total', 'product_name', 'product_stock'
        ]

    def get_total(self, obj):
        return obj.get_total()

    def get_product_name(self, obj):
        return obj.product_id.name if obj.product_id else None

    def get_product_stock(self, obj):
        return obj.product_id.stock if obj.product_id else 0

    # Validations
    def validate(self, data):s
        if data.get('cantidad', 0) <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que 0")

        if data.get('precio', 0) <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que 0")

        # Validation of the relationship between user and product
        if data.get('user_id') and data.get('product_id'):
            if data['user_id'].fk_company != data['product_id'].fk_company:
                raise serializers.ValidationError(
                    "El producto no pertenece a la empresa del usuario"
                )

            # Validation of stock availability
            if data['product_id'].stock < data['cantidad']:
                raise serializers.ValidationError(
                    f"Stock insuficiente. Disponible: {data['product_id'].stock}"
                )

        return data

class BasketTempDetailSerializer(BasketTempSerializer):
    # View details of the basket
    product_details = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta(BasketTempSerializer.Meta):
        fields = BasketTempSerializer.Meta.fields + ['product_details', 'user_details']

    def get_product_details(self, obj):
        if not obj.product_id:
            return None
        return {
            'name': obj.product_id.name,
            'category': obj.product_id.category,
            'description': obj.product_id.description,
            'stock': obj.product_id.stock,
            'iva': obj.product_id.iva
        }

    def get_user_details(self, obj):
        if not obj.user_id:
            return None
        return {
            'name': obj.user_id.name,
            'email': obj.user_id.email,
            'company': obj.user_id.fk_company.name if obj.user_id.fk_company else None
        }

class InvoiceItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = [
            'id', 'invoice', 'product', 'quantity', 'price',
            'product_name', 'subtotal'
        ]

    def get_product_name(self, obj):
        return obj.product.name if obj.product else None

    def get_subtotal(self, obj):
        return obj.price * obj.quantity