"""
Admin configuration for business type models.
"""

from django.contrib import admin
from .models import Type

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Type model.
    Simple admin with basic list display and search fields.
    """
    list_display = ('id', 'name_type')
    search_fields = ('name_type',)