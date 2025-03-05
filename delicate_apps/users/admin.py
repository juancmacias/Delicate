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
        if not change:  # Si es un nuevo usuario
            # Guardar la contraseña original
            password = obj.password
            # Hashear la contraseña
            obj.set_password(password)
            # Guardar el objeto original (en lugar de crear uno nuevo)
            obj.save()
        else:
            # Si es una actualización, verificar si la contraseña ha cambiado
            if form.cleaned_data.get('password') != form.initial.get('password'):
                obj.set_password(form.cleaned_data.get('password'))
            obj.save()