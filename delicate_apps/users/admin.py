from django.contrib import admin
from django import forms
from .models import User

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        help_texts = {
            'username': 'Opcional. Se generará automáticamente a partir del email si se deja en blanco.',
        }

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    # Mostrar campos en la lista del panel de administración
    list_display = ('id', 'name', 'email', 'username', 'roll', 'active')
    # Habilitar una barra de búsqueda
    search_fields = ('name', 'email', 'username', 'roll')
    # Añadir filtros laterales
    list_filter = ('active', 'roll')
    # Ordenar los registros de forma predeterminada
    ordering = ('id',)
    # Restringir ciertos campos a solo lectura
    readonly_fields = ('id',)
    # Organizar los campos en secciones dentro del formulario de edición
    fieldsets = (
        ('Información Personal', {
            'fields': ('name', 'email', 'username', 'password', 'roll')
        }),
        ('Estado y Relaciones', {
            'fields': ('active', 'company', 'groups', 'user_permissions')
        }),
        ('Información del Sistema', {
            'fields': ('id',),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Personalizar cómo se guarda el modelo desde el admin"""
        # El método create_user del UserManager se encargará de generar un username
        # si no se ha proporcionado uno
        super().save_model(request, obj, form, change)