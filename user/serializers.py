from abc import ABC

from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from .models import User
from equipment.serializers import EquipmentSerializer
from application.rent_application.serializers import RentApplicationSerializer
from application.renter_application.serializers import RenterApplicationSerializer
from application.release_application.serializers import ReleaseApplicationSerializer


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
    rented_equipments = EquipmentSerializer(many=True, read_only=True)
    rent_applications = RentApplicationSerializer(many=True, read_only=True)

    renter_applications = RenterApplicationSerializer(many=True, read_only=True)
    release_applications = ReleaseApplicationSerializer(many=True, read_only=True)
    received_rent_applications = RentApplicationSerializer(many=True, read_only=True)

    owned_equipments = EquipmentSerializer(many=True, read_only=True)


    class Meta:
        model = User
        fields = '__all__'
