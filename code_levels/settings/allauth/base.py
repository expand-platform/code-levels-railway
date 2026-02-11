import os

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.environ.get("GOOGLE_AUTH_CLIENT_ID", ""),
            "secret": os.environ.get("GOOGLE_AUTH_CLIENT_SECRET", ""),
            "key": "",
        },
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
        "SCOPE": [
            "profile",
            "email",
        ],
        "LOGIN_HINT": "",
        "PROMPT": "select_account",
        "SKIP_CONFIRMATION": True,
    }
}

ACCOUNT_FORMS = {
    "login": "platform_web.forms.CustomLoginForm",
    "signup": "platform_web.forms.custom_signup_form.CustomSignupForm",
    "socialaccount_signup": "platform_web.forms.custom_social_signup_form.CustomSocialSignupForm",
}

SITE_ID = 1
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "projects"
LOGOUT_REDIRECT_URL = "home"
# Use custom social account adapter to autogenerate username
SOCIALACCOUNT_ADAPTER = "platform_web.forms.custom_social_account_adapter.CustomSocialAccountAdapter"
