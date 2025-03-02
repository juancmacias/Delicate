from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Company(models.Model):
    direction = models.CharField(max_length=255)
    cif = models.CharField(max_length=20, unique=True)
    phone = models.IntegerField()
    mail = models.EmailField(max_length=255)

    def __str__(self):
        return self.name
