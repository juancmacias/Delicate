from django.contrib import admin
from .models import Invoice, InvoiceItem

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'payment_form', 'neto', 'fk_user', 'fk_company', 'fk_type')
    list_filter = ('date', 'fk_company', 'fk_type')
    search_fields = ('id', 'payment_form')
    date_hierarchy = 'date'

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'product', 'quantity', 'price', 'get_subtotal')
    list_filter = ('invoice', 'product')
    search_fields = ('invoice__id', 'product__name')