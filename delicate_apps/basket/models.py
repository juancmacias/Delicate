from django.db import models
from delicate_apps.users.models import User
from delicate_apps.store.models import Product

class BasketTemp(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name="basket_items",
        verbose_name="Usuario",
    )

    product_id = models.ForeignKey(
        StoreProduct,
        on_delete=models.CASCADE,
        db_column='product_id',
        related_name="basket_items",
        verbose_name="Producto",
    )

    cantidad = models.IntegerField(verbose_name="Cantidad")
    precio = models.FloatField(verbose_name="Precio")
    temp_date = models.DateTimeField(verbose_name="Fecha")

    def __str__(self):
        return f"item de {self.user_ide} - {self.product_id}"

    class Meta:
        verbose_name = "Item de cesta temporal"
        verbose_name_plural = "Items de cesta temporal"
        db_table = "basket_temp"

    def get_total(self):
        return self.cantidad * self.precio
