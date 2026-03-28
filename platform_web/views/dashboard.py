import re

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import activate, gettext as _

from api.models import UserProfile


class SettingsView(LoginRequiredMixin, View):
    template_name = "website/dashboard/pages/settings.html"

    def get(self, request):
        user_profile = getattr(request.user, "user_profile", None)
        return render(
            request,
            self.template_name,
            {
                "user_profile": user_profile,
                "user": request.user,
            },
        )

    #! Race condition possible if user submits multiple requests simultaneously. Consider adding locking or atomic transactions if this becomes an issue.
    def post(self, request):
        username = request.POST.get("username", "").strip()
        if username:
            # Username validation
            reserved_usernames = {"admin", "root", "system", "null", "undefined", "user", "users", "username", "profile", "settings", "dashboard", "account", "accounts", "support", "help", "contact", "api", "apis", "webmaster", "hostmaster", "postmaster", "me", "you", "they", "we", "us", "them", "he", "she", "it", "his", "her", "its", "their", "my", "mine", "your", "yours", "our", "ours", "theirs", "this", "that", "these", "those", "who", "what", "where", "when", "why", "how"}
            username_pattern = r"^[a-zA-Z0-9_]+$"
            min_length = 3
            max_length = 30

            # Block encoded/invisible characters
            invisible_pattern = r"[\u200B-\u200D\uFEFF]"
            html_entity_pattern = r"&[a-zA-Z0-9#]+;"
            unicode_escape_pattern = r"\\u[0-9A-Fa-f]{4}|\\x[0-9A-Fa-f]{2}"

            # Stricter underscore rules
            if username.lower() in reserved_usernames:
                messages.error(
                    request,
                    "This username is reserved, sorry :( Please choose another.",
                )
            elif not re.match(username_pattern, username):
                messages.error(
                    request,
                    "Username must contain only letters, numbers, and underscores.",
                )
            elif username.isdigit():
                messages.error(
                    request,
                    "Username cannot be numbers only.",
                )
            elif re.search(invisible_pattern, username):
                messages.error(
                    request,
                    "Username cannot contain invisible characters.",
                )
            elif re.search(html_entity_pattern, username):
                messages.error(
                    request,
                    "Username cannot contain HTML entities.",
                )
            elif re.search(unicode_escape_pattern, username):
                messages.error(
                    request,
                    "Username cannot contain unicode escape sequences.",
                )
            elif username.startswith("_") or username.endswith("_"):
                messages.error(
                    request,
                    "Username cannot start or end with an underscore.",
                )
            elif "__" in username:
                messages.error(
                    request,
                    "Username cannot contain consecutive underscores.",
                )
            elif not (min_length <= len(username) <= max_length):
                messages.error(
                    request,
                    f"Username must be {min_length}-{max_length} characters long.",
                )
            elif (
                User.objects.filter(username=username)
                .exclude(pk=request.user.pk)
                .exists()
            ):
                messages.error(request, "Username already taken.")
            else:
                request.user.username = username
                request.user.save()
                messages.success(request, "Username updated successfully.")
        
        user_profile = getattr(request.user, "user_profile", None)
        # language preference
        language = request.POST.get("language", "").strip()
        if language:
            valid_codes = [code for code, name in getattr(settings, 'LANGUAGES', [])]
            if language in valid_codes:
                if user_profile is None:
                    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.interface_language = language
                user_profile.save(update_fields=["interface_language"])
                # apply for current session
                try:
                    request.session[settings.LANGUAGE_COOKIE_NAME] = language
                except Exception:
                    pass
                activate(language)
                messages.success(request, _("Language preference saved."))
        
        return render(
            request,
            self.template_name,
            {
                "user_profile": user_profile,
                "user": request.user,
            },
        )
