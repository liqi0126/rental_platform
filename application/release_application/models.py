from django.db import models

from user.models import User
from equipment.models import Equipment
from application.models import Application

from django.conf import settings
# Create your models here.


class ReleaseApplication(Application):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='release_applications')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='release_applications')
