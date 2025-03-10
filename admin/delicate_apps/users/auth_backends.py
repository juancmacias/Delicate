from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Buscar al usuario por su email
            user = User.objects.get(email=email)
            
            # Verificar la contraseña y si el usuario está activo
            if user.check_password(password) and user.is_active:
                # Verificar si el usuario tiene acceso al admin (basado en su rol)
                if user.roll in ['admin', 'manager', 'employee']:  # Roles permitidos
                    return user
                else:
                    # Lanzar un error personalizado si el usuario no tiene un rol permitido
                    raise ValidationError("You do not have permission to access the admin panel.")
            else:
                # Lanzar un error si la contraseña es incorrecta o el usuario no está activo
                raise ValidationError("Invalid credentials or inactive account.")
        except User.DoesNotExist:
            # Lanzar un error si el usuario no existe
            raise ValidationError("User does not exist.")
        except Exception as e:
            # Capturar cualquier otro error inesperado
            raise ValidationError(f"An error occurred: {str(e)}")

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None