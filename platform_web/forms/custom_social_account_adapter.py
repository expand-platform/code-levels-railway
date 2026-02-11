from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.utils.text import slugify
import uuid

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if not user.username:
            base_username = slugify(user.email.split('@')[0]) if user.email else 'user'
            username = base_username
            from django.contrib.auth import get_user_model
            User = get_user_model()
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            user.username = username
        return user
