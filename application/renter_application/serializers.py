from rest_framework import serializers
from .models import RenterApplication


class RenterApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenterApplication
        fields = '__all__'
