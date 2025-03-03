from django.contrib import admin
from .models import StoreProduct

@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'net_price', 'iva', 'fk_company', 'fk_type')
    list_filter = ('category', 'fk_company', 'fk_type')
    search_fields = ('name', 'description', 'category')