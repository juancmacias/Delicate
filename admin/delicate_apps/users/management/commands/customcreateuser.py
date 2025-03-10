# users/management/commands/customsuperuser.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import getpass
from delicate_apps.company.models import Company

User = get_user_model()  # Obtiene el modelo de usuario personalizado

class Command(BaseCommand):
    help = 'Crea un usuario personalizado con diferentes roles (admin, manager, employee, customer)'

    def handle(self, *args, **kwargs):
        print('Creando usuario personalizado...')
        email = input("Email: ").strip()
        name = input("Name: ").strip()
        roll = input("Roll (admin/manager/employee/customer): ").strip().lower()  # Convertir a minúsculas
        company_id = input("Company ID: ").strip()
        
        # Validar campos obligatorios
        if not email or not name or not roll or not company_id:
            self.stdout.write(self.style.ERROR('Todos los campos son obligatorios'))
            return

        # Validar el rol
        if roll not in ['admin', 'manager', 'employee', 'customer']:
            self.stdout.write(self.style.ERROR('Rol no válido. Debe ser admin, manager, employee o customer.'))
            return

        # Solicitar la contraseña dos veces y comparar
        password = getpass.getpass("Password: ").strip()
        password_confirm = getpass.getpass("Confirm Password: ").strip()

        if password != password_confirm:
            self.stdout.write(self.style.ERROR('Las contraseñas no coinciden. Inténtalo de nuevo.'))
            return

        try:
            # Obtener la instancia de Company
            company = Company.objects.get(id=company_id)

            # Crear el usuario según su rol
            if roll == 'admin':
                # Crear un superusuario
                user = User.objects.create_superuser(
                    email=email,
                    password=password,
                    name=name,
                    roll=roll,
                    company=company,
                    username=email  # Usar el email como username
                )
                self.stdout.write(self.style.SUCCESS(f'Superusuario creado: {user.email}'))
            else:
                # Crear un usuario normal
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    name=name,
                    roll=roll,
                    company=company,
                    username=email  # Usar el email como username
                )
                self.stdout.write(self.style.SUCCESS(f'Usuario creado: {user.email} (Rol: {roll})'))
        except Company.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No existe una compañía con el ID {company_id}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al crear el usuario: {e}'))