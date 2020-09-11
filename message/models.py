from django.db import models
from django.utils import timezone
from django.conf import settings


class Message(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    text = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_equipments')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rented_equipments')

    class Meta:
        ordering = ['created_at']
        app_label = 'message'

