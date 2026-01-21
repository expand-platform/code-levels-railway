from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms

class CustomSocialSignupForm(SocialSignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("email", None)

    def save(self, request):
        user = super().save(request)
        return user
