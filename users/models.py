# users/models.py
import uuid

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class UserToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(default=timezone.now)
