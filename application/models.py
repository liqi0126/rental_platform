from django.db import models
from django.utils import timezone

from user.models import User
# Create your models here.


class Application(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    description = models.TextField()


    class Status(models.TextChoices):
        UNAPPROVED = 'UNA'
        ACCEPTED = 'ACC'
        REJECTED = 'REJ'

    status = models.CharField(max_length=3,
                              choices=Status.choices,
                              default=Status.UNAPPROVED)

    comments = models.TextField(default='')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['created_at']
        abstract = True
