from django.contrib import admin

from .models import BasketTemp

@admin.register(BasketTemp)
class BasketTempAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'product_id', 'cantidad', 'precio', 'temp_date')
    list_filter = ('user_id', 'temp_date')
    search_fields = ('user_id__username', 'product_id__name')
    date_hierarchy = 'temp_date'
