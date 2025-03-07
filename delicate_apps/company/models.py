from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import re
from django.core.exceptions import ValidationError
class Company(models.Model):
    name = models.CharField(max_length=255)
    direction = models.CharField(max_length=255)
    cif = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    mail = models.EmailField(max_length=255)
    def clean(self):
        if not re.match(r'^\d+$', self.phone):  # Solo permite números
            raise ValidationError({'phone': 'El teléfono solo puede contener números.'})
    def __str__(self):
        return self.name
