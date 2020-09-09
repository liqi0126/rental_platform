from abc import ABC

from rest_framework import serializers
from equipment.serializers import EquipmentSerializer
from .models import User
from rest_auth.registration.serializers import RegisterSerializer


class MyRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    address = serializers.CharField(max_length=1000, required=False)

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'address': self.validated_data.get('address', '')
        }


class UserSerializer(serializers.ModelSerializer):
    owned_equipments = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
