from django.contrib import admin
from .models import StoreProduct

@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'net_price', 'get_stock_display', 'iva', 'fk_company', 'fk_type')
    list_filter = ('category', 'fk_company', 'fk_type')
    search_fields = ('name', 'category')
    readonly_fields = ('get_stock_info',)

    def get_stock_display(self, obj):
        """Muestra el stock en la lista de productos"""
        stock_actual = obj.get_stock_actual()
        return f"{stock_actual} unidades"
    get_stock_display.short_description = "Unidades disponibles"

    def get_stock_info(self, obj):
        """Muestra información detallada del stock"""
        if not obj.id:
            return "Producto nuevo - Stock no disponible"
        
        stock_actual = obj.get_stock_actual()
        vendidas = obj.get_unidades_vendidas()
        
        info = f"Stock inicial: {obj.stock_inicial} unidades\n"
        info += f"Unidades vendidas: {vendidas}\n"
        info += f"Stock actual: {stock_actual} unidades\n"
        
        return info
    get_stock_info.short_description = "Información de Stock"

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
        ('Imágenes y Metadata', {
            'fields': ('image',)
        }),
        ('Relaciones', {
            'fields': ('fk_company', 'fk_type')
        }),
    )