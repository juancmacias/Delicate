from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from delicate_apps.company.models import Company

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        #extra_fields.setdefault('username', email.split('@')[0])  # Añade esta línea
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')
    email = models.EmailField(max_length=255, unique=True)
    roll = models.CharField(max_length=50, choices=ROLE_CHOICES, default='employee')
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    # Configurar related_name único para groups y user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  # Nombre único para la relación inversa
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # Nombre único para la relación inversa
        related_query_name='user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'company']    
    objects = UserManager()
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        if self.roll == 'admin':
            return True
        elif self.roll == 'manager':
            return perm in ['view_user', 'change_user', 'add_user']
        elif self.roll == 'employee':
            return perm in ['view_user']
        return False

    def has_module_perms(self, app_label):
        return True