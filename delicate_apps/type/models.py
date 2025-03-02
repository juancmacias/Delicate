from django.db import models

class Type(models.Model):
    id = models.AutoField(primary_key=True)
    name_type = models.CharField(max_length=30, verbose_name="Tipo de comercio")

    def __str__(self):
        return self.name_type

        class Meta:
            verbose_name = "Tipo de comercio"
            verbose_name_plural = "Tipos de comercio"
            db_table = 'type'