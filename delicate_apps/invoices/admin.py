from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'get_total']
    
    def get_total(self, obj):
        return f"{obj.get_total():.2f}€"
    get_total.short_description = 'Total'
    
    def has_add_permission(self, request, obj=None):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    # Fields to display in list view
    list_display = ('id', 'date', 'fk_user', 'get_total_display', 'payment_form', 'export_csv_button')
    list_filter = ('date', 'payment_form', 'fk_company')
    search_fields = ('id', 'fk_user__name', 'fk_user__email')
    date_hierarchy = 'date'
    inlines = [InvoiceItemInline]
    
    # Make all fields readonly
    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_total_display(self, obj):
        return f"{obj.get_total():.2f}€"
    get_total_display.short_description = 'Total'

    def export_csv_button(self, obj):
        """Añade un botón para exportar la factura a CSV"""
        url = reverse('export-invoice-csv', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">Exportar CSV</a>', url)
    export_csv_button.short_description = 'Exportar CSV'
    export_csv_button.allow_tags = True

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'product', 'quantity', 'price', 'get_total_display')
    list_filter = ('invoice__date',)
    search_fields = ('invoice__id', 'product__name')
    
    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]
        
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
        
    def get_total_display(self, obj):
        return f"{obj.get_total():.2f}€"
    get_total_display.short_description = 'Total'