from dataclasses import dataclass
from django.contrib.auth.models import User

@dataclass
class UserRepository:
    @staticmethod
    def get_empty_profiles():
        return User.objects.filter(user_profile__isnull=True)
    
    