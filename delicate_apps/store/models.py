from django.db import models
from delicate_apps.company.models import Company
from delicate_apps.type.models import Type

class StoreProduct(models.Model):
    id = models.AutoField(primary_key=True)
    iva = models.FloatField(verbose_name='IVA')
    category = models.CharField(max_length=50, verbose_name='Categoría')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.CharField(max_length=250, verbose_name='Descripción')
    amount = models.CharField(max_length=100, verbose_name='Cantidad')
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

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'store_products'
    
    def get_total_price(self):
        return self.net_price * (1 + (self.iva / 100))
