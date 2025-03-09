from rest_framework import serializers
from .models import BasketTemp
from delicate_apps.invoices.models import Invoice, InvoiceItem
from delicate_apps.store.models import StoreProduct
from decimal import Decimal

class BasketTempSerializer(serializers.ModelSerializer):
    """Basic serializer for basket items with calculated fields."""
    # Calculated fields
    total = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_stock = serializers.SerializerMethodField()
    formatted_price = serializers.SerializerMethodField()
    formatted_total = serializers.SerializerMethodField()

    class Meta:
        model = BasketTemp
        fields = [
            'id', 'user_id', 'product_id', 'cantidad', 'precio',
            'temp_date', 'status', 'total', 'product_name', 'product_stock',
            'formatted_price', 'formatted_total'
        ]

    def get_total(self, obj):
        """Get total price for the basket item."""
        return round(Decimal(str(obj.get_total())), 2)

    def get_product_name(self, obj):
        """Get product name."""
        return obj.product_id.name if obj.product_id else None

    def get_product_stock(self, obj):
        """Get available product stock."""
        return obj.product_id.stock if obj.product_id else 0

    def get_formatted_price(self, obj):
        """Get formatted price with currency symbol."""
        return f"{round(Decimal(str(obj.precio)), 2):.2f} €"

    def get_formatted_total(self, obj):
        """Get formatted total with currency symbol."""
        return f"{self.get_total(obj):.2f} €"

    # Validations
    def validate(self, data):
        """Validate basket data."""
        if data.get('cantidad', 0) <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que 0")

        if data.get('precio', 0) <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que 0")

        if data.get('user_id') and data.get('product_id'):
            # Check if product belongs to user's company
            if data['user_id'].company != data['product_id'].fk_company:
                raise serializers.ValidationError(
                    "El producto no pertenece a la empresa del usuario"
                )

            # Check if product stock is sufficient
            if data['product_id'].stock < data['cantidad']:
                raise serializers.ValidationError(
                    f"Stock insuficiente. Disponible: {data['product_id'].stock}"
                )

        return data

class BasketTempDetailSerializer(BasketTempSerializer):
    """Extended serializer with additional product and user details."""
    product_details = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta(BasketTempSerializer.Meta):
        fields = BasketTempSerializer.Meta.fields + ['product_details', 'user_details']

    def get_product_details(self, obj):
        """Get detailed product information."""
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
        """Get detailed user information."""
        if not obj.user_id:
            return None
        return {
            'name': obj.user_id.name,
            'email': obj.user_id.email,
            'company': obj.user_id.company.name if obj.user_id.company else None
        }

class BasketTempHistorySerializer(BasketTempSerializer):
    """Serializer for purchase history that includes invoice information."""
    invoice_info = serializers.SerializerMethodField()

    class Meta(BasketTempSerializer.Meta):
        fields = BasketTempSerializer.Meta.fields + ['invoice_info']

    def get_invoice_info(self, obj):
        """Get invoice information for this purchased item."""
        # Find invoice that contains this product for this user
        invoice_items = InvoiceItem.objects.filter(
            product=obj.product_id,
            invoice__fk_user=obj.user_id
        )
        if invoice_items:
            # Get the most recent invoice item
            latest_item = invoice_items.order_by('-invoice__date').first()
            return {
                'invoice_id': latest_item.invoice.id,
                'date': latest_item.invoice.date,
                'payment_form': latest_item.invoice.payment_form
            }
        return None

class InvoiceItemSerializer(serializers.ModelSerializer):
    """Serializer for invoice items."""
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
        """Get product name."""
        return obj.product.name if obj.product else None

    def get_subtotal(self, obj):
        """Calculate subtotal for this item."""
        return round(Decimal(str(obj.price * obj.quantity)), 2)

    def get_formatted_price(self, obj):
        """Get formatted price with currency symbol."""
        return f"{round(Decimal(str(obj.price)), 2):.2f} €"

    def get_formatted_subtotal(self, obj):
        """Get formatted subtotal with currency symbol."""
        return f"{self.get_subtotal(obj):.2f} €"