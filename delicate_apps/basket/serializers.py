from rest_framework import serializers
from .models import BasketTemp
from delicate_apps.invoices.models import Invoice, InvoiceItem
from delicate_apps.store.models import StoreProduct
from decimal import Decimal

class BasketTempSerializer(serializers.ModelSerializer):
    # Inputs calculated fields
    total = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_stock = serializers.SerializerMethodField()
    formatted_price = serializers.SerializerMethodField()
    formatted_total = serializers.SerializerMethodField()

    class Meta:
        model = BasketTemp
        fields = [
            'id', 'user_id', 'product_id', 'cantidad', 'precio',
            'temp_date', 'total', 'product_name', 'product_stock',
            'formatted_price', 'formatted_total'
        ]

    def get_total(self, obj):
        return round(Decimal(str(obj.get_total())), 2)

    def get_product_name(self, obj):
        return obj.product_id.name if obj.product_id else None

    def get_product_stock(self, obj):
        return obj.product_id.stock if obj.product_id else 0

    def get_formatted_price(self, obj):
        return f"{round(Decimal(str(obj.precio)), 2):.2f} €"

    def get_formatted_total(self, obj):
        return f"{self.get_total(obj):.2f} €"

    # Validations
    def validate(self, data):
        if data.get('cantidad', 0) <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que 0")

        if data.get('precio', 0) <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que 0")

        if data.get('user_id') and data.get('product_id'):
            if data['user_id'].company != data['product_id'].fk_company:
                raise serializers.ValidationError(
                    "El producto no pertenece a la empresa del usuario"
                )

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
            'iva': obj.product_id.iva,
            'precio': f"{round(Decimal(str(obj.precio)), 2):.2f} €"
        }

    def get_user_details(self, obj):
        if not obj.user_id:
            return None
        return {
            'name': obj.user_id.name,
            'email': obj.user_id.email,
            'company': obj.user_id.company.name if obj.user_id.company else None
        }

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
        return round(Decimal(str(obj.price * obj.quantity)), 2)

    def get_formatted_price(self, obj):
        return f"{round(Decimal(str(obj.price)), 2):.2f} €"

    def get_formatted_subtotal(self, obj):
        return f"{self.get_subtotal(obj):.2f} €"