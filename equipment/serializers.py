from rest_framework import serializers
from .models import Equipment

from application.release_application.serializers import ReleaseApplicationSerializer
from application.rent_application.serializers import RentApplicationSerializer


class EquipmentSerializer(serializers.ModelSerializer):
    release_applications = ReleaseApplicationSerializer(many=True, read_only=True)
    rent_applications = RentApplicationSerializer(many=True, read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'
