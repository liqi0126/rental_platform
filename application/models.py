from django.db import models
from django.utils import timezone

from user.models import User
# Create your models here.


class Application(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    description = models.TextField()

    class ApplicationStatus(models.TextChoices):
        UNAPPROVED = 'UNA'
        ACCEPTED = 'ACC'
        REJECTED = 'REJ'

    status = models.CharField(max_length=3,
                              choices=ApplicationStatus.choices,
                              default=ApplicationStatus.UNAPPROVED)

    comments = models.TextField()

    def __str__(self):
        return self.id

    class Meta:
        ordering = ['created_at']
        abstract = True
