"""
Invoice models for managing customer purchases.
"""

from django.db import models
from decimal import Decimal
from delicate_apps.users.models import User
from delicate_apps.company.models import Company
from delicate_apps.type.models import Type
from delicate_apps.store.models import StoreProduct

class Invoice(models.Model):
    """
    Invoice model for tracking completed purchases.
    Represents the header of an invoice with related customer and payment info.
    """
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name='Fecha')
    payment_form = models.CharField(max_length=100, verbose_name='Forma de pago')
    neto = models.FloatField(verbose_name='Importe neto')

    # Relations
    fk_type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        db_column='fk_type',
        related_name='invoices',
        verbose_name='Tipo'
    )
    fk_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='fk_user',
        related_name='invoices',
        verbose_name='Usuario'
    )
    fk_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        db_column='fk_company',
        related_name='invoices',
        verbose_name='Empresa'
    )

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        db_table = 'invoices'

    def __str__(self):
        return f'Factura {self.id} - {self.date}'

    def get_total(self):
        """Calculate total amount including IVA"""
        # Sum all invoice items to get the total
        if hasattr(self, 'items'):
            total = sum(item.get_total() for item in self.items.all())
            return round(Decimal(str(total)), 2)
        return round(Decimal(str(self.neto)), 2)
        
    def get_iva_amount(self):
        """Calculate total IVA amount for the invoice."""
        if hasattr(self, 'items'):
            total_iva = sum(item.get_iva_amount() for item in self.items.all())
            return round(Decimal(str(total_iva)), 2)
        return Decimal('0')

class InvoiceItem(models.Model):
    """
    Invoice item model for individual products in an invoice.
    Each item represents a product line in the invoice with its quantity and price.
    """
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Factura'
    )
    product = models.ForeignKey(
        StoreProduct,
        on_delete=models.CASCADE,
        verbose_name='Producto'
    )
    quantity = models.IntegerField(verbose_name='Cantidad')
    price = models.FloatField(verbose_name='Precio unitario')
    
    class Meta:
        verbose_name = 'Detalle de factura'
        verbose_name_plural = 'Detalles de factura'
        db_table = 'invoice_items'
        
    def __str__(self):
        return f'Item {self.id} - Factura {self.invoice.id}'
        
    def get_total(self):
        """Calculate the total for this item without IVA"""
        return round(Decimal(str(self.price * self.quantity)), 2)
        
    def get_iva_amount(self):
        """Calculate the IVA amount for this item"""
        if hasattr(self.product, 'iva'):
            iva_rate = Decimal(str(self.product.iva)) / 100
            return round(self.get_total() * iva_rate, 2)
        return Decimal('0')
        
    def get_total_with_iva(self):
        """Calculate the total for this item with IVA"""
        return self.get_total() + self.get_iva_amount()