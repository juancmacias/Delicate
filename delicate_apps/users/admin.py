from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib import admin
from users.forms import CustomLoginForm

# Sobrescribe el formulario de autenticación del admin
admin.site.login_form = CustomLoginForm
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'roll', 'company')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'roll', 'company', 'active')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    # Mostrar campos en la lista del panel de administración
    list_display = ('id', 'name', 'email', 'username', 'roll', 'active')
    # Habilitar una barra de búsqueda
    search_fields = ('name', 'email', 'username', 'roll')
    # Añadir filtros laterales
    list_filter = ('active', 'roll')
    # Ordenar los registros de forma predeterminada
    ordering = ('id',)
    # Segunda barrera de seguridad para evitar acceso de clientes al admin.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.exclude(roll='customer')  # Excluir clientes del admin
    # Campos para el formulario de creación
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'username', 'company', 'roll', 'password1', 'password2'),
        }),
    )
    
    # Campos para el formulario de edición
    fieldsets = (
        ('Información Personal', {
            'fields': ('email', 'name', 'username', 'password', 'roll')
        }),
        ('Estado y Relaciones', {
            'fields': ('active', 'company', 'groups', 'user_permissions')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
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
