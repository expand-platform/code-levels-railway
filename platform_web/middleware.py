from django.http import HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.views import redirect_to_login


# middleware.py
# from .permissions import get_entitlements

# class PlanMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response  # Django passes this in, it's the next middleware or view

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             request.entitlements = get_entitlements(request.user)
#             request.plan = request.entitlements['plan_name']
#         else:
#             request.entitlements = None
#             request.plan = 'anonymous'

#         response = self.get_response(request)  # pass to next layer
#         return response


class AdminStaffOnlyMiddleware:
    """
    Restrict /cp/ access to authenticated staff users only.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Always allow static & media
        if path.startswith("/static/") or path.startswith("/media/"):
            return self.get_response(request)

        # Restrict control panel
        if path.startswith("/cp/"):
            user = request.user

            if not user.is_authenticated:
                return redirect_to_login(path, settings.LOGIN_URL)

            if not user.is_staff:
                return HttpResponseForbidden("Forbidden")

        return self.get_response(request)



# class PreferredLanguageMiddleware:
#     """
#     If a logged-in user has a preferred language set on their profile,
#     apply it for the current session and activate translations for the
#     request. This keeps the UI language consistent with user settings.
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         path = request.path

#         # Always allow static & media
#         if path.startswith("/static/") or path.startswith("/media/"):
#             return self.get_response(request)

#         user = getattr(request, 'user', None)
#         if user and user.is_authenticated:
#             profile = getattr(user, 'user_profile', None)
#             if profile and getattr(profile, 'interface_language', None):
#                 lang = profile.interface_language
#                 try:
#                     request.session[settings.LANGUAGE_COOKIE_NAME] = lang
#                 except Exception:
#                     # session may not be available in some contexts
#                     pass
#                 activate(lang)
#                 request.LANGUAGE_CODE = lang

#         return self.get_response(request)