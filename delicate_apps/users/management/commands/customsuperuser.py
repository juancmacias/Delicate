# users/management/commands/createsuperuser.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import getpass
from delicate_apps.company.models import Company

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea un superusuario personalizado'

    def handle(self, *args, **kwargs):
        print('Creando superusuario customizado...')
        email = input("Email**: ")
        password = getpass.getpass("Password: ")
        name = input("Name: ")
        roll = input("Roll (admin/manager/employee): ")
        username = email
        company_id = input("Company ID: ")

        try:
            # Obtener la instancia de Company
            company = Company.objects.get(id=company_id)
            user = User.objects.create_superuser(
                email=email,
                password=password,
                name=name,
                roll=roll,
                company=company,
                username=username
                
            )
            self.stdout.write(self.style.SUCCESS(f'Superusuario creado: {user.email}'))
        except Company.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No existe una compañía con el ID {company_id}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al crear el superusuario: {e}'))