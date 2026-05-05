from django.core.management.base import BaseCommand
from api.services.UserProfileService import UserProfileService


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        UserProfileService.create_missing_profiles()

        self.stdout.write(self.style.SUCCESS("Profiles created"))
