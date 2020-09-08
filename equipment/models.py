from django.db import models
from django.utils import timezone
from phone_field import PhoneField


from user.models import User
# Create your models here.


class Equipment(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)

    address = models.CharField(max_length=1000)
    email = models.EmailField()
    phone = PhoneField(blank=True, help_text='Contact phone number')
    description = models.TextField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_equipments')

    class EquipmentStatus(models.TextChoices):
        UNRELEASED = 'UNR'
        UNAPPROVED = 'UNA'
        AVAILABLE = 'AVA'
        RENTED = 'REN'
        RETURNED = 'RET'

    status = models.CharField(max_length=3, choices=EquipmentStatus.choices, default=EquipmentStatus.UNRELEASED)

    # if it is rented
    current_tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rented_equipments', blank=True, null=True)
    lease_term_begin = models.DateTimeField(blank=True, null=True)
    lease_term_end = models.DateTimeField(blank=True, null=True)
    user_comments = models.TextField(blank=True, null=True)

    # foreign key related name:
    #   release_applications
    #   rent_applications

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
        app_label = 'equipment'


