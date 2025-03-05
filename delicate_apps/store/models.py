from django.db import models
from delicate_apps.company.models import Company
from delicate_apps.type.models import Type
from django.db.models import Sum

class StoreProduct(models.Model):
    id = models.AutoField(primary_key=True)
    iva = models.FloatField(verbose_name='IVA')
    category = models.CharField(max_length=50, verbose_name='Categoría')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.CharField(max_length=250, verbose_name='Descripción')
    amount = models.CharField(max_length=100, verbose_name='Cantidad')
    stock_inicial = models.IntegerField(verbose_name='Stock inicial', default=0)
    image = models.CharField(max_length=255, verbose_name='Imagen', blank=True, null=True)
    net_price = models.FloatField(verbose_name='Precio neto')
    fk_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        db_column='fk_company',
        related_name='products',
        verbose_name='Empresa'
    )
    fk_type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        db_column='fk_type',
        related_name='products',
        verbose_name='Tipo de comercio'
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'store_products'

    def __str__(self):
        return self.name

    def get_total_price(self):
        return self.net_price * (1 + (self.iva / 100))

    def get_unidades_vendidas(self):
        """Calcula el total de unidades vendidas"""
        from delicate_apps.invoices.models import InvoiceItem
        vendidas = InvoiceItem.objects.filter(product=self).aggregate(
            total=Sum('quantity'))['total'] or 0
        return vendidas

    def get_stock_actual(self):
        """Calcula el stock actual basado en inventario inicial menos ventas"""
        return self.stock_inicial - self.get_unidades_vendidas()

    def add_stock(self, cantidad):
        """Añade unidades al stock inicial"""
        if cantidad > 0:
            self.stock_inicial += cantidad
            self.save()
            return True
        return False

    def remove_stock(self, cantidad):
        """Resta unidades del stock inicial"""
        stock_actual = self.get_stock_actual()
        if cantidad > 0 and stock_actual >= cantidad:
            self.stock_inicial -= cantidad
            self.save()
            return True
        return False