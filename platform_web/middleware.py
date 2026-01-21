from django.shortcuts import redirect
from django.http import HttpResponseForbidden

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
                return redirect(f"/accounts/login/?next={path}")

            if not user.is_staff:
                return HttpResponseForbidden("Forbidden")

        return self.get_response(request)
