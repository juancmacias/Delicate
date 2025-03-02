from rest_framework import serializers
from django.contrib.auth.models import get_user_model
from rest_framework.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        """ The password field will be accepted as input (when writing data), 
        but will not be included in the response (when serializing data). """
        extra_kwargs = {
            'password': {'write_only': True}
        }

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.name
        token['roll'] = user.roll
        return token        