from allauth.account.forms import LoginForm
from dataclasses import dataclass


@dataclass
class AllAuthFiedls:
    login: str = "login"
    password: str = "password"


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[AllAuthFiedls.login].widget.attrs.update(
            {"placeholder": "Email or Username", "class": "form-control"}
        )
        self.fields[AllAuthFiedls.password].widget.attrs.update(
            {"placeholder": "Password", "class": "form-control"}
        )

    def clean(self):
        try:
            return super().clean()
        except Exception:
            self.add_error(None, "Invalid login or password.")
            raise

    def login(self, *args, **kwargs):
        return super().login(*args, **kwargs)
