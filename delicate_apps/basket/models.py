"""
Basket temporary items model for shopping cart functionality.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from delicate_apps.users.models import User
from delicate_apps.store.models import StoreProduct

class BasketTemp(models.Model):
    """
    Temporary basket item for shopping cart.
    Tracks products added to cart before purchase completion.
    """
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
    # False = pending in cart, True = purchased
    status = models.BooleanField(
        verbose_name="Estado de la compra",
        default=False,
        help_text="True si la compra fue realizada, False si está pendiente"
    )
    
    class Meta:
        verbose_name = "Item de cesta temporal"
        verbose_name_plural = "Items de cesta temporal"
        db_table = "basket_temp_items"
        ordering = ['-temp_date']
        
    def __str__(self):
        return f"Item de {self.user_id} - {self.product_id}"

    def clean(self):
        """
        Validate basket item before saving.
        """
        # Validate that quantity is positive
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
                self.precio = self.product_id.net_price

    def save(self, *args, **kwargs):
        """Override save to ensure validation and price calculation."""
        # Set price based on product if not defined
        if not self.precio and self.product_id:
            self.precio = self.product_id.net_price
            
        self.full_clean()
        super().save(*args, **kwargs)

    def get_total(self):
        """Calculate total price without IVA."""
        if self.precio is None:
            self.precio = self.product_id.net_price
            self.save()
        return self.cantidad * self.precio

    def get_iva(self):
        """Calculate IVA (tax) amount."""
        if hasattr(self.product_id, 'iva'):
            total = float(self.get_total()) * (float(self.product_id.iva) / 100)
            return round(total, 2)
        return 0

    def get_total_with_iva(self):
        """Calculate total price including IVA."""
        total = float(self.get_total()) + float(self.get_iva())
        return round(total, 2)