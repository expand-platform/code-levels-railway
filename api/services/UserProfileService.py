from api.repositories.UserRepository import UserRepository
from api.models.UserProfile import UserProfile


class UserProfileService:
    @staticmethod
    def create_missing_profiles():
        """ create user profiles for users that don't have one yet """
        users = UserRepository.get_empty_profiles()

        for user in users:
            UserProfile.objects.get_or_create(user=user)
