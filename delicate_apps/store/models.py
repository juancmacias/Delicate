from django.db import models
from delicate_apps.company.models import Company
from delicate_apps.type.models import Type
from django.db.models import Sum
from django.utils import timezone
from cloudinary.models import CloudinaryField

class StoreProduct(models.Model):
    # Basic product info
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.CharField(max_length=250, verbose_name='Descripción')
    category = models.CharField(max_length=50, verbose_name='Categoría')
    
    # Pricing and taxes
    net_price = models.FloatField(verbose_name='Precio neto')
    iva = models.FloatField(verbose_name='IVA')
    
    # Stock management (keeping legacy fields but using stock as primary)
    amount = models.CharField(max_length=100, verbose_name='Cantidad (obsoleto)')
    stock_inicial = models.IntegerField(verbose_name='Stock inicial (obsoleto)', default=0)
    stock = models.IntegerField(verbose_name='Stock disponible', default=0)
    
    # Media
    image = CloudinaryField(
        'image', 
        blank=False,
        null=False, 
        help_text='Imagen del producto',
        transformation=[
            {'width': 500, 'height': 500, 'crop': 'limit'},
            {'quality': 'auto'},
            {'fetch_format': 'auto'}
        ]
    )
    
    # Relations
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
        """Calculate price with IVA included"""
        return self.net_price * (1 + (self.iva / 100))
    
    def get_formatted_price(self):
        """Return formatted price with two decimals and € symbol"""
        return f"{self.net_price:.2f} €"
    
    def get_formatted_total_price(self):
        """Return price with IVA formatted with two decimals and € symbol"""
        return f"{self.get_total_price():.2f} €"
    
    def get_unidades_vendidas(self):
        """Calculate total units sold"""
        from delicate_apps.invoices.models import InvoiceItem
        vendidas = InvoiceItem.objects.filter(product=self).aggregate(
            total=Sum('quantity'))['total'] or 0
        return vendidas
    
    def add_stock(self, cantidad, user=None, notes=""):
        """Add units to stock and register the movement"""
        if cantidad > 0:
            old_stock = self.stock
            self.stock += cantidad
            self.save()
            
            # Register movement
            StockMovement.objects.create(
                product=self,
                movement_type='add',
                quantity=cantidad,
                previous_stock=old_stock,
                new_stock=self.stock,
                user=user,
                notes=notes
            )
            return True
        return False

    def remove_stock(self, cantidad, user=None, notes=""):
        """Remove units from stock and register the movement"""
        if cantidad > 0 and self.stock >= cantidad:
            old_stock = self.stock
            self.stock -= cantidad
            self.save()
            
            # Register movement
            StockMovement.objects.create(
                product=self,
                movement_type='remove',
                quantity=cantidad,
                previous_stock=old_stock,
                new_stock=self.stock,
                user=user,
                notes=notes
            )
            return True
        return False
    
    def get_stock_movements(self, limit=10):
        """Return the latest stock movements for this product"""
        return StockMovement.objects.filter(product=self).order_by('-created_at')[:limit]


class StockMovement(models.Model):
    """Model to register stock movements"""
    MOVEMENT_TYPES = [
        ('add', 'Entrada'),
        ('remove', 'Salida'),
        ('sale', 'Venta'),
        ('adjustment', 'Ajuste'),
        ('initial', 'Stock Inicial'),
    ]
    
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(StoreProduct, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    previous_stock = models.IntegerField()
    new_stock = models.IntegerField()
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Movimiento de Stock'
        verbose_name_plural = 'Movimientos de Stock'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_movement_type_display()} de {self.quantity} unidades para {self.product.name}"