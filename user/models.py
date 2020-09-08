from django.db import models
from django.utils import timezone
from phone_field import PhoneField

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))

        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=1000)
    phone = PhoneField(blank=True, help_text='Contact phone number')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

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

