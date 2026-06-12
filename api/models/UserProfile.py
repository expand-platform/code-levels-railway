import uuid

from django.db import models
from django.contrib.auth.models import User

from platform_web.models.user.PaidPlan import PaidPlan


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

    wakatime_api_key = models.CharField(max_length=255, blank=True, null=True)
    
    paid_plan = models.ForeignKey(
        PaidPlan, on_delete=models.CASCADE, related_name="user_plan", null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username} with telegram ID {self.telegram_user_id} and tg first name {self.telegram_first_name}"
    
    def update_telegram_info(self, telegram_user_id, telegram_first_name):
        self.telegram_user_id = telegram_user_id
        self.telegram_first_name = telegram_first_name
        self.is_token_verified = True
        self.save()
        
    def save_wakatime_api_key(self, api_key):
        self.wakatime_api_key = api_key
        self.save()
