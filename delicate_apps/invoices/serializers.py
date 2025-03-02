from rest_framework import serializers
from .models import Invoice
from delicate_apps.type.serializers import TypeSerializer
from delicate_apps.users.serializers import UserSerializer
from delicate_apps.company.serializers import CompanySerializer

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceDetailSerializer(serializers.ModelSerializer):
    fk_type = TypeSerializer(read_only=True)
    fk_user = UserSerializer(read_only=True)
    fk_company = CompanySerializer(read_only=True)
    
    class Meta:
        model = Invoice
        fields = '__all__'