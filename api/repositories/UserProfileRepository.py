from api.models.UserProfile import UserProfile


class UserProfileRepository:
    @staticmethod
    def create_profile_for_user(user):
        return UserProfile.objects.create(user=user)
