from django.db import models

from user.models import User
from equipment.models import Equipment
from application.models import Application
from rest_framework import serializers
# Create your models here.


class RentApplication(Application):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='rent_applications')
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_applications')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_rent_applications')


class RentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentApplication
        fields = '__all__'
