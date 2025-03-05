from django.contrib import admin
from django.utils.html import format_html
from .models import StoreProduct, StockMovement
from django import forms

class StockMovementInline(admin.TabularInline):
    model = StockMovement
    extra = 0
    readonly_fields = ('movement_type', 'quantity', 'previous_stock', 'new_stock', 'user', 'created_at')
    fields = ('movement_type', 'quantity', 'previous_stock', 'new_stock', 'user', 'notes', 'created_at')
    can_delete = False
    max_num = 0
    verbose_name = "Movimiento de stock"
    verbose_name_plural = "Historial de movimientos"
    
    def has_add_permission(self, request, obj=None):
        return False

class StockManagementForm(forms.ModelForm):
    """Form for more intuitive stock management"""
    add_stock = forms.IntegerField(
        label="Añadir unidades", 
        required=False, 
        min_value=0,
        help_text="Número de unidades a añadir al stock actual"
    )
    
    remove_stock = forms.IntegerField(
        label="Retirar unidades", 
        required=False, 
        min_value=0,
        help_text="Número de unidades a retirar del stock actual"
    )
    
    stock_notes = forms.CharField(
        label="Notas", 
        required=False, 
        widget=forms.Textarea(attrs={'rows': 2}),
        help_text="Motivo del cambio de stock (opcional)"
    )
    
    class Meta:
        model = StoreProduct
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        add = cleaned_data.get('add_stock') or 0
        remove = cleaned_data.get('remove_stock') or 0
        current_stock = self.instance.stock if self.instance.pk else 0
        
        if add > 0 and remove > 0:
            raise forms.ValidationError(
                "No puedes añadir y retirar stock simultáneamente, utiliza solo uno de los campos."
            )
        
        if remove > current_stock:
            raise forms.ValidationError(
                f"No puedes retirar {remove} unidades. El stock actual es de {current_stock} unidades."
            )
        
        return cleaned_data

@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    form = StockManagementForm
    list_display = ('id', 'name', 'category', 'get_price_display', 'get_price_with_iva_display', 
                   'stock', 'get_stock_status', 'fk_company')
    list_filter = ('category', 'fk_company', 'fk_type')
    search_fields = ('name', 'category', 'description')
    readonly_fields = ('stock', 'stock_inicial', 'amount')
    inlines = [StockMovementInline]
    
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
            'fields': ('name', 'description', 'category')
        }),
        ('Precios e Impuestos', {
            'fields': ('net_price', 'iva')
        }),
        ('Gestión de Stock', {
            'fields': ('stock', 'add_stock', 'remove_stock', 'stock_notes'),
            'description': 'El stock actual se actualiza automáticamente cuando se realizan ventas o ajustes manuales.'
        }),
        ('Imagen', {
            'fields': ('image',),
            'classes': ('collapse',),
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