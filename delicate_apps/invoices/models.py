from django.db import models
from delicate_apps.users.models import User
from delicate_apps.company.models import Company
from delicate_apps.type.models import Type

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name='Fecha')
    payment_form = models.CharField(max_length=100, verbose_name='Forma de pago')
    neto = models.FloatField(verbose_name='Importe neto')

    fk_type =models.ForeignKey(
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

    def __str__(self):
        return f'Factura {self.id}'

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        db_table = 'invoices'

    def get_total(self):
        return self.neto
