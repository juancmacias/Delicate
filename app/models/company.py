import app.models as models
from sqlmodel import SQLModel, Field

class Company(models.Model):
    name = models.CharField(max_length=255)
    direction = models.CharField(max_length=255)
    cif = models.CharField(max_length=20, unique=True)
    phone = models.IntegerField()
    mail = models.EmailField(max_length=255)

    def str(self):
        return self.name