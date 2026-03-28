from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "telegram_user_id",
        "telegram_first_name",
        "telegram_connection_token",
        "is_token_verified",
        "interface_language",
    )
