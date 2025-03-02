from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'payment_form', 'neto', 'fk_type', 'fk_user', 'fk_company')
    list_filter = ('date', 'payment_form', 'fk_type', 'fk_company')
    search_fields = ('id', 'payment_form')
    date_hierarchy = 'date'
