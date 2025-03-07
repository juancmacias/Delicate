from django.contrib import admin
from .models import StoreProduct

@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'net_price', 'get_stock_display', 'iva', 'fk_company', 'fk_type')
    list_filter = ('category', 'fk_company', 'fk_type')
    search_fields = ('name', 'category', 'description')
    readonly_fields = ('stock', 'stock_inicial', 'amount', 'image_preview')
    inlines = [StockMovementInline]
    
    def image_preview(self, obj):
        """Display a preview of the product image"""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 300px;" />', obj.image.url)
        return "No image available"
    image_preview.short_description = "Vista previa"
    
    def get_price_display(self, obj):
        """Display formatted net price"""
        return obj.get_formatted_price()
    get_price_display.short_description = "Precio neto"
    
    def get_price_with_iva_display(self, obj):
        """Display formatted price with IVA"""
        return obj.get_formatted_total_price()
    get_price_with_iva_display.short_description = "Precio con IVA"
    
    def get_stock_status(self, obj):
        """Display stock status with colors"""
        if obj.stock <= 0:
            return format_html(
                '<span style="color: #ff0000; font-weight: bold;">Sin stock</span>'
            )
        elif obj.stock <= 5:
            return format_html(
                '<span style="color: #ffa500; font-weight: bold;">Stock bajo</span>'
            )
        else:
            return format_html(
                '<span style="color: #008000;">Stock disponible</span>'
            )
    get_stock_status.short_description = "Estado"
    
    def save_model(self, request, obj, form, change):
        """Handle stock changes when saving the model"""
        add_stock = form.cleaned_data.get('add_stock') or 0
        remove_stock = form.cleaned_data.get('remove_stock') or 0
        notes = form.cleaned_data.get('stock_notes') or ""
        
        # Save object first so it has an ID if it's new
        super().save_model(request, obj, form, change)
        
        # If it's a new object, register an initial stock movement
        if not change:
            StockMovement.objects.create(
                product=obj,
                movement_type='initial',
                quantity=obj.stock,
                previous_stock=0,
                new_stock=obj.stock,
                user=request.user if request.user.is_authenticated else None,
                notes="Stock inicial al crear el producto"
            )
        
        # Process stock changes
        if add_stock > 0:
            obj.add_stock(add_stock, request.user, notes)
        elif remove_stock > 0:
            obj.remove_stock(remove_stock, request.user, notes)
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'category', 'description')
        }),
        ('Precios e Impuestos', {
            'fields': ('net_price', 'iva')
        }),
        ('Stock', {
            'fields': ('stock_inicial', 'get_stock_info')
        }),
        ('Imagen', {
            'fields': ('image', 'image_preview'),
            'description': 'Sube una imagen para el producto (obligatorio)',
        }),
        ('Relaciones', {
            'fields': ('fk_company', 'fk_type')
        }),
    )

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'movement_type', 'quantity', 'previous_stock', 
                   'new_stock', 'user', 'created_at')
    list_filter = ('movement_type', 'product__category', 'created_at')
    search_fields = ('product__name', 'notes')
    readonly_fields = ('product', 'movement_type', 'quantity', 'previous_stock', 
                      'new_stock', 'user', 'created_at')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False  # Stock movements should not be modified