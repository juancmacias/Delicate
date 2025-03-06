from django.db import models
from django.conf import settings
from django.conf import settings
from delicate_apps.company.models import Company
from delicate_apps.type.models import Type
from django.db.models import Sum
from django.utils import timezone
from cloudinary.models import CloudinaryField

class StoreProduct(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, verbose_name='Categoría')
    category = models.CharField(max_length=50, verbose_name='Categoría')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.CharField(max_length=250, verbose_name='Descripción')
    
    # Pricing and taxes
    net_price = models.FloatField(verbose_name='Precio neto')
    iva = models.FloatField(verbose_name='IVA')
    
    # Stock management
    amount = models.CharField(max_length=100, verbose_name='Cantidad (obsoleto)', blank=True, null=True)
    stock_inicial = models.IntegerField(verbose_name='Stock inicial', default=0)
    # Stock management
    amount = models.CharField(max_length=100, verbose_name='Cantidad (obsoleto)', blank=True, null=True)
    stock_inicial = models.IntegerField(verbose_name='Stock inicial', default=0)
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


    def get_formatted_price(self):
        """Formatted net price display"""
        """Formatted net price display"""
        return f"{self.net_price:.2f} €"


    def get_formatted_total_price(self):
        """Formatted price with IVA"""
        total_price = self.get_total_price()
        return f"{total_price:.2f} €"

    def get_total_price(self):
        """Calculate total price with IVA"""
        return self.net_price * (1 + (self.iva / 100))

        """Formatted price with IVA"""
        total_price = self.get_total_price()
        return f"{total_price:.2f} €"

    def get_total_price(self):
        """Calculate total price with IVA"""
        return self.net_price * (1 + (self.iva / 100))

    def get_unidades_vendidas(self):
        """Calcula el total de unidades vendidas"""
        from delicate_apps.invoices.models import InvoiceItem
        vendidas = InvoiceItem.objects.filter(product=self).aggregate(
            total=Sum('quantity'))['total'] or 0
        return vendidas


    def add_stock(self, cantidad, user=None, notes=""):
        """Añade unidades al stock"""
        """Añade unidades al stock"""
        if cantidad > 0:
            previous_stock = self.stock
            previous_stock = self.stock
            self.stock += cantidad
            self.save()
            
            # Crear movimiento de stock
            # Crear movimiento de stock
            StockMovement.objects.create(
                product=self,
                movement_type='add',
                quantity=cantidad,
                previous_stock=previous_stock,
                previous_stock=previous_stock,
                new_stock=self.stock,
                user=user,
                notes=notes
            )
            return True
        return False

    def remove_stock(self, cantidad, user=None, notes=""):
        """Resta unidades del stock"""
        """Resta unidades del stock"""
        if cantidad > 0 and self.stock >= cantidad:
            previous_stock = self.stock
            previous_stock = self.stock
            self.stock -= cantidad
            self.save()
            
            # Crear movimiento de stock
            # Crear movimiento de stock
            StockMovement.objects.create(
                product=self,
                movement_type='remove',
                quantity=cantidad,
                previous_stock=previous_stock,
                previous_stock=previous_stock,
                new_stock=self.stock,
                user=user,
                notes=notes
            )
            return True
        return False

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('initial', 'Stock inicial'),
        ('add', 'Añadir stock'),
        ('remove', 'Retirar stock'),
        ('initial', 'Stock inicial'),
        ('add', 'Añadir stock'),
        ('remove', 'Retirar stock'),
    ]

    product = models.ForeignKey(
        StoreProduct, 
        on_delete=models.CASCADE, 
        related_name='stock_movements',
        verbose_name='Producto'
    )
    movement_type = models.CharField(
        max_length=20, 
        choices=MOVEMENT_TYPES, 
        verbose_name='Tipo de movimiento'
    )
    quantity = models.IntegerField(verbose_name='Cantidad')
    previous_stock = models.IntegerField(verbose_name='Stock anterior')
    new_stock = models.IntegerField(verbose_name='Stock nuevo')

    product = models.ForeignKey(
        StoreProduct, 
        on_delete=models.CASCADE, 
        related_name='stock_movements',
        verbose_name='Producto'
    )
    movement_type = models.CharField(
        max_length=20, 
        choices=MOVEMENT_TYPES, 
        verbose_name='Tipo de movimiento'
    )
    quantity = models.IntegerField(verbose_name='Cantidad')
    previous_stock = models.IntegerField(verbose_name='Stock anterior')
    new_stock = models.IntegerField(verbose_name='Stock nuevo')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Usuario'
        blank=True,
        verbose_name='Usuario'
    )
    notes = models.TextField(
        null=True, 
        blank=True, 
        verbose_name='Notas'
    )
    created_at = models.DateTimeField(
        default=timezone.now, 
        verbose_name='Fecha de creación'
    )

    notes = models.TextField(
        null=True, 
        blank=True, 
        verbose_name='Notas'
    )
    created_at = models.DateTimeField(
        default=timezone.now, 
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = 'Movimiento de stock'
        verbose_name_plural = 'Movimientos de stock'
        verbose_name = 'Movimiento de stock'
        verbose_name_plural = 'Movimientos de stock'
        ordering = ['-created_at']


    def __str__(self):
        return f"Movimiento de {self.quantity} unidades de {self.product.name} - {self.get_movement_type_display()}"
        return f"Movimiento de {self.quantity} unidades de {self.product.name} - {self.get_movement_type_display()}"