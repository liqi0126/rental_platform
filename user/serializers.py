from abc import ABC

from rest_framework import serializers
from equipment.serializers import EquipmentSerializer
from .models import User
from rest_auth.registration.serializers import RegisterSerializer


class MyRegisterSerializer(RegisterSerializer):
    is_superuser = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)

    def get_cleaned_data(self):
        is_superuser = self.validated_data.get('is_superuser', False)
        print(type(is_superuser))

        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            # 'is_superuser': self.validated_data.get('is_superuser', False),
            # 'is_staff': self.validated_data.get('is_staff', False)
        }


class UserSerializer(serializers.ModelSerializer):
    owned_equipments = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
