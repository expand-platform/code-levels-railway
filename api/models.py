from django.db import models
from django.contrib.auth.models import User

import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    telegram_connection_token = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False
    )
    telegram_user_id = models.BigIntegerField(null=True, blank=True)


    def __str__(self):
        return f"Profile for {self.user.username}"
