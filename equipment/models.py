from django.db import models
from django.utils import timezone
from phone_field import PhoneField


from user.models import User
from django.conf import settings
# Create your models here.


class Equipment(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)

    address = models.CharField(max_length=1000)
    email = models.EmailField()
    phone = PhoneField(blank=True, help_text='Contact phone number')
    description = models.TextField()

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_equipments')

    class EquipmentStatus(models.TextChoices):
        UNRELEASED = 'UNR'
        UNAPPROVED = 'UNA'
        AVAILABLE = 'AVA'
        RENTED = 'REN'
        RETURNED = 'RET'

    status = models.CharField(max_length=3, choices=EquipmentStatus.choices, default=EquipmentStatus.UNRELEASED)

    # foreign key related name:
    #   release_applications
    #   rent_applications

    # if it is rented
    # current_tenant: rent_applications.get(applying=True).hirer
    # lease_term_begin: rent_applications.get(applying=True).lease_term_begin
    # user_comments: rent_applications.get(applying=True).user_comments



    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
        app_label = 'equipment'

