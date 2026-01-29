from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms

class CustomSocialSignupForm(SocialSignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("email", None)

    def save(self, request):
        user = super().save(request)
        # Autogenerate username from email
        email = user.email
        base_username = email.split("@")[0] if email else "user"
        username = base_username
        from django.contrib.auth import get_user_model
        User = get_user_model()
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username
        user.save()
        return user
