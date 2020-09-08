from django.db import models

from user.models import User
from application.models import Application
# Create your models here.


class RenterApplication(Application):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='renter_applications')

