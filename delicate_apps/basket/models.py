from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from delicate_apps.users.models import User
from delicate_apps.store.models import StoreProduct
from decimal import Decimal

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

            # Set price if not defined
            if not self.precio:
                self.precio = float(round(Decimal(str(self.product_id.net_price)), 2))

    def save(self, *args, **kwargs):
        # Set price based on product if not defined
        if not self.precio and self.product_id:
            self.precio = float(round(Decimal(str(self.product_id.net_price)), 2))
            
        self.full_clean()
        super().save(*args, **kwargs)

    def get_total(self):
        """Calculate total without IVA"""
        if self.precio is None:
            self.precio = float(round(Decimal(str(self.product_id.net_price)), 2))
            self.save()
        total = self.cantidad * self.precio
        return round(Decimal(str(total)), 2)

    def get_iva(self):
        """Calculate IVA amount"""
        if hasattr(self.product_id, 'iva'):
            total = float(self.get_total()) * (float(self.product_id.iva) / 100)
            return round(Decimal(str(total)), 2)
        return Decimal('0.00')

    def get_total_with_iva(self):
        """Calculate total with IVA"""
        total = float(self.get_total()) + float(self.get_iva())
        return round(Decimal(str(total)), 2)

    def format_price(self, value):
        """Format price with two decimals and € symbol"""
        return f"{round(Decimal(str(value)), 2):.2f}€"