from django.db import models

from user.models import User
from application.models import Application
from rest_framework import serializers
# Create your models here.


class RenterApplication(Application):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='renter_applications', blank=True, null=True)


class RenterApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenterApplication
        fields = '__all__'
