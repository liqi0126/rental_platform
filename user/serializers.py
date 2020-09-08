from rest_framework import serializers
from equipment.serializers import EquipmentSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    owned_equipments = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
