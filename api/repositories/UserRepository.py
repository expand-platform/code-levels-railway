from django.contrib.auth.models import User


class UserRepository:
    @staticmethod
    def get_empty_profiles():
        return User.objects.filter(user_profile__isnull=True)
