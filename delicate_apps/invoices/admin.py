"""
Admin interface configuration for invoice models.
"""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    """
    Inline admin for invoice items.
    Shows invoice line items within the invoice admin page.
    """
    model = InvoiceItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'get_total']
    
    def get_total(self, obj):
        """Display formatted total for the item."""
        return f"{obj.get_total():.2f}€"
    get_total.short_description = 'Total'
    
    def has_add_permission(self, request, obj=None):
        """Disable adding items directly through admin."""
        return False
        
    def has_delete_permission(self, request, obj=None):
        """Disable deleting items through admin."""
        return False

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Invoice model.
    Shows invoice details and provides CSV export functionality.
    """
    # Fields to display in list view
    list_display = ('id', 'date', 'fk_user', 'get_total_display', 'payment_form')
    list_display = ('id', 'date', 'fk_user', 'get_total_display', 'payment_form', 'export_csv_button')
    list_filter = ('date', 'payment_form', 'fk_company')
    search_fields = ('id', 'fk_user__name', 'fk_user__email')
    date_hierarchy = 'date'
    inlines = [InvoiceItemInline]
    
    # Make all fields readonly
    def get_readonly_fields(self, request, obj=None):
        """Make all fields readonly since invoices shouldn't be modified."""
        return [field.name for field in self.model._meta.fields]

    def has_add_permission(self, request):
        """Disable adding invoices through admin."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable deleting invoices through admin."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable editing invoices through admin."""
        return False

    def get_total_display(self, obj):
        """Display formatted total amount."""
        return f"{obj.get_total():.2f}€"
    get_total_display.short_description = 'Total'

    def export_csv_button(self, obj):
        """Add export to CSV button for each invoice."""
        url = reverse('admin-export-invoice-csv', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_self">Exportar CSV</a>', url)
    export_csv_button.short_description = 'Exportar CSV'
    export_csv_button.allow_tags = True

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for InvoiceItem model.
    Read-only view of invoice line items.
    """
    list_display = ('id', 'invoice', 'product', 'quantity', 'price', 'get_total_display')
    list_filter = ('invoice__date',)
    search_fields = ('invoice__id', 'product__name')
    
    def get_readonly_fields(self, request, obj=None):
        """Make all fields readonly since invoice items shouldn't be modified."""
        return [field.name for field in self.model._meta.fields]
        
    def has_add_permission(self, request):
        """Disable adding invoice items through admin."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Allow deleting invoice items through admin for correction purposes."""
        return True

    def has_change_permission(self, request, obj=None):
        """Disable editing invoice items through admin."""
        return False
        
    def get_total_display(self, obj):
        """Display formatted total for the item."""
        return f"{obj.get_total():.2f}€"
    get_total_display.short_description = 'Total'