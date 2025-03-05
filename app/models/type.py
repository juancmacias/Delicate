import app.models as models
from sqlmodel import SQLModel, Field


class User(models.Model, SQLModel, table=True):

    company = models.ForeignKey(models.Company, on_delete=models.CASCADE, related_name='users')
    email = models.EmailField(max_length=255, unique=True)
    roll = models.CharField(max_length=50, default='employee')
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    # Configurar related_name único para groups y user_permissions
    groups = models.ManyToManyField(
        models.Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  # Nombre único para la relación inversa
        related_query_name='user',
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'company']
    objects = UserManager()

    def str(self):
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