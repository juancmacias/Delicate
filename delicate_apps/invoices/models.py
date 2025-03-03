from django.db import models
from delicate_apps.users.models import User
from delicate_apps.company.models import Company
from delicate_apps.type.models import Type
from delicate_apps.store.models import StoreProduct
from decimal import Decimal, ROUND_HALF_UP

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name='Fecha')
    payment_form = models.CharField(max_length=100, verbose_name='Forma de pago')
    neto = models.FloatField(verbose_name='Importe neto')

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
        return f'Factura {self.id}'

    def get_total(self):
        total = sum(item.get_subtotal() for item in self.items.all())
        return round(Decimal(str(total)), 2)

    def format_price(self, value):
        return f"{round(Decimal(str(value)), 2):.2f}€"

class InvoiceItem(models.Model):
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
        related_name='invoice_items',
        verbose_name='Producto'
    )
    quantity = models.IntegerField(verbose_name="Cantidad")
    price = models.FloatField(verbose_name="Precio")
    
    class Meta:
        verbose_name = 'Detalle de factura'
        verbose_name_plural = 'Detalles de facturas'
        db_table = 'invoice_items'
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} en factura {self.invoice.id}"
    
    def get_subtotal(self):
        return self.quantity * self.price
        return round(Decimal(str(subtotal)), 2)