from django.db import models

from user.models import User
from equipment.models import Equipment
from application.models import Application

from django.conf import settings
# Create your models here.


class RentApplication(Application):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='rent_applications')
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rent_applications')
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_rent_applications', null=True, blank=True)
    applying = models.BooleanField(default=False)

    lease_term_begin = models.DateTimeField(blank=True, null=True)
    lease_term_end = models.DateTimeField(blank=True, null=True)
    user_comments = models.TextField(blank=True, null=True)
