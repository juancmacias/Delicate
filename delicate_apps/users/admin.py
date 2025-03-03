from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 1. Mostrar campos en la lista del panel de administración
    list_display = ('id', 'name', 'email', 'roll', 'active')
    # 2. Habilitar una barra de búsqueda
    search_fields = ('name', 'email', 'roll')
    # 3. Añadir filtros laterales
    list_filter = ('active', 'roll')
    # 4. Ordenar los registros de forma predeterminada
    ordering = ('id',)
    # 5. Restringir ciertos campos a solo lectura
    readonly_fields = ('id',)
    # 6. Organizar los campos en secciones dentro del formulario de edición
    fieldsets = (
        ('Información Personal', {
            'fields': ('name', 'email', 'password', 'roll')
        }),
        ('Estado y Relaciones', {
            'fields': ('active', 'company', 'groups', 'user_permissions')
        }),
        ('Identificador', {
            'fields': ('id',),
            'classes': ('collapse',),
        }),
    )
