import app.models as models
from sqlmodel import SQLModel, Field
from fastapi.utils import timezone

class BasketTemp(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        models.User,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name="basket_temp_items",
        verbose_name="Usuario",
    )
    product_id = models.ForeignKey(
        models.StoreProduct,
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

    def str(self):
        return f"Item de {self.user_id} - {self.product_id}"

    
        # Validate that quantity is positive


    def save(self, args, **kwargs):
        # Set price based on product if not defined
        if not self.precio and self.product_id:
            self.precio = self.product_id.net_price

        self.full_clean()
        super().save(args, *kwargs)

    def get_total(self):
        """Calculate total without IVA"""
        if self.precio is None:
            self.precio = self.product_id.net_price
            self.save()
        return self.cantidad * self.precio

    def get_iva(self):
        """Calculate IVA amount"""
        if hasattr(self.product_id, 'iva'):
            total = float(self.get_total()) * (float(self.product_id.iva) / 100)
            return round(total, 2)
        return 0

    def get_total_with_iva(self):
        """Calculate total with IVA"""
        total = float(self.get_total()) + float(self.get_iva())
        return round(total, 2)
