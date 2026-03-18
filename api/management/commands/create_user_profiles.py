from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import UserProfile


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = User.objects.filter(user_profile__isnull=True)

        for user in users:
            UserProfile.objects.get_or_create(user=user)

        self.stdout.write(self.style.SUCCESS("Profiles created"))
