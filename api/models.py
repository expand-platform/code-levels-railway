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
    telegram_first_name = models.CharField(max_length=150, null=True, blank=True)
    is_token_verified = models.BooleanField(default=False)


    def __str__(self):
        return f"Profile for {self.user.username} with telegram user ID {self.telegram_user_id} and telegram first name {self.telegram_first_name}"
    
    def update_telegram_info(self, telegram_user_id, telegram_first_name):
        self.telegram_user_id = telegram_user_id
        self.telegram_first_name = telegram_first_name
        self.is_token_verified = True
        self.save()
