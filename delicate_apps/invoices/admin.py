from django.contrib import admin
from .models import Invoice, InvoiceItem

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'payment_form', 'get_neto_formatted', 'fk_user', 'fk_company', 'fk_type')
    list_filter = ('date', 'fk_company', 'fk_type')
    search_fields = ('id', 'payment_form')
    date_hierarchy = 'date'

    def get_neto_formatted(self, obj):
        return f"{obj.neto:.2f}€"
    get_neto_formatted.short_description = 'Importe neto'

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'product', 'quantity', 'get_price_formatted', 'get_subtotal_formatted')
    list_filter = ('invoice', 'product')
    search_fields = ('invoice__id', 'product__name')

    def get_price_formatted(self, obj):
        return f"{obj.price:.2f}€"
    get_price_formatted.short_description = 'Precio (Unidad)'

    def get_subtotal_formatted(self, obj):
        return f"{obj.get_subtotal():.2f}€"
    get_subtotal_formatted.short_description = 'Subtotal'