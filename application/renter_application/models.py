from django.db import models
from django.conf import settings

from user.models import User
from application.models import Application
# Create your models here.


class RenterApplication(Application):
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='renter_applications')