from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from delicate_apps.users.models import User
from delicate_apps.store.models import StoreProduct

class BasketTemp(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name="basket_temp_items",
        verbose_name="Usuario",
    )
    product_id = models.ForeignKey(
        StoreProduct,
        on_delete=models.CASCADE,
        db_column='product_id',
        related_name="basket_temp_products",
        verbose_name="Producto",
    )
    cantidad = models.IntegerField(verbose_name="Cantidad")
    precio = models.FloatField(verbose_name="Precio", blank=True, null=True)
    temp_date = models.DateTimeField(
        verbose_name="Fecha",
        default=timezone.now
    )

    class Meta:
        verbose_name = "Item de cesta temporal"
        verbose_name_plural = "Items de cesta temporal"
        db_table = "basket_temp_items"
        ordering = ['-temp_date']

    def __str__(self):
        return f"Item de {self.user_id} - {self.product_id}"

    def clean(self):
        if not self.cantidad or self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que 0")

        if self.product_id:
            # Validate that the product belongs to the user's company
            if self.user_id and self.user_id.company != self.product_id.fk_company:
                raise ValidationError(
                    "El producto no pertenece a la empresa del usuario"
                )

            # Establish the price if it's not set
            if not self.precio:
                self.precio = self.product_id.net_price

    def save(self, *args, **kwargs):
        # If the price is not set, use the product's net price
        if not self.precio and self.product_id:
            self.precio = self.product_id.net_price
            
        self.full_clean()
        super().save(*args, **kwargs)

    def get_total(self):
        if self.precio is None:
            self.precio = self.product_id.net_price
            self.save()
        return self.cantidad * self.precio

    def get_iva(self):
        if hasattr(self.product_id, 'iva'):
            return self.get_total() * (self.product_id.iva / 100)
        return 0

    def get_total_with_iva(self):
        return self.get_total() + self.get_iva()