from django import forms
from django.contrib import admin
from .models import BasketTemp

class BasketTempForm(forms.ModelForm):
    class Meta:
        model = BasketTemp
        # Exclude price field from the form
        exclude = ('precio',)

@admin.register(BasketTemp)
class BasketTempAdmin(admin.ModelAdmin):
    form = BasketTempForm
    list_display = ('id', 'user_id', 'product_id', 'cantidad', 'precio', 'temp_date', 'status')
    list_filter = ('temp_date', 'user_id', 'status')
    search_fields = ('user_id__email', 'product_id__name')
    date_hierarchy = 'temp_date'
    readonly_fields = ('id', 'user_id', 'product_id', 'cantidad', 'precio', 'temp_date', 'status')

    # Calculate price automatically when saving
    def save_model(self, request, obj, form, change):
        if obj.product_id:
            obj.precio = obj.product_id.get_total_price()
        super().save_model(request, obj, form, change)
        
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False