"""
Serializers for business type models.
"""

from rest_framework import serializers
from .models import Type

class TypeSerializer(serializers.ModelSerializer):
    """
    Serializer for Type model.
    Simple serializer that includes all fields.
    """
    class Meta:
        model = Type
        fields = '__all__'