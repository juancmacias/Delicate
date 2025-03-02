from django.contrib import admin
from .models import Type

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_type')
    search_fields = ('name_type',)
