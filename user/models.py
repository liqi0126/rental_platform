from django.db import models
from django.utils import timezone

from phone_field import PhoneField
# Create your models here.


class Administrator(models.Model):
    admin = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)

    class Meta:
        app_label = 'user'




class User(models.Model):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    created_at = models.DateTimeField(default=timezone.now)

    address = models.CharField(max_length=1000)
    email = models.EmailField()
    phone = PhoneField(blank=True, help_text='Contact phone number')

    # foreign key related name:
    #   rent_applications
    #   rented_equipments

    # for renter
    is_renter = models.BooleanField(default=False)

    # foreign key related name:
    #   renter_applications
    #   release_applications
    #   received_rent_applications
    #   owned_equipments

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['created_at']
        app_label = 'user'

