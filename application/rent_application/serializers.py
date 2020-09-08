from rest_framework import serializers
from .models import RentApplication


class RentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentApplication
        fields = '__all__'
