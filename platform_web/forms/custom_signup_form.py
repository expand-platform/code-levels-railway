from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model



class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)

    def save(self, request):
        user = super().save(request)
        base_username = self.cleaned_data["email"].split("@")[0]
        username = base_username
        User = get_user_model()
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username
        user.save()
        return user
