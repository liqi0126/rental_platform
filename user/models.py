from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phone_field import PhoneField
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    created_at = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=1000)
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

    class Meta:
        ordering = ['created_at']
        app_label = 'user'

