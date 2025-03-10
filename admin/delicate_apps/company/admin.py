from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # 1. Mostrar campos en la lista del panel de administración
    list_display = ('id', 'direction', 'cif', 'phone', 'mail')
    # 2. Habilitar una barra de búsqueda para ciertos campos
    search_fields = ('direction', 'cif', 'mail')
    # 3. Añadir filtros laterales
    list_filter = ('direction',)
    # 4. Definir el orden predeterminado de los registros
    ordering = ('id',)
    # 5. Restringir campos a solo lectura si no deberían editarse directamente
    readonly_fields = ('id',)
    # 6. Organizar campos en secciones dentro del formulario de edición
    fieldsets = (
        ('Información Principal', {
            'fields': ('direction', 'cif', 'phone', 'mail'),
        }),
        ('Metadatos', {
            'fields': ('id',),
            'classes': ('collapse',),
        }),
    )
