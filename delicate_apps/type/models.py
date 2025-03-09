"""
Type models for business type classification.
"""

from django.db import models

class Type(models.Model):
    """
    Business type classification model.
    Used to categorize businesses by their commercial activity.
    """
    id = models.AutoField(primary_key=True)
    name_type = models.CharField(max_length=30, verbose_name="Tipo de comercio")

    def __str__(self):
        return self.name_type

    class Meta:
        verbose_name = "Tipo de comercio"
        verbose_name_plural = "Tipos de comercio"
        db_table = 'type'