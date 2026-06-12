from typing import Callable, Optional

from django.http import HttpResponseForbidden, HttpRequest, HttpResponse
from django.conf import settings
from django.contrib.auth.views import redirect_to_login

from api.models.UserProfile import UserProfile
from platform_web.models.user.PaidPlan import PaidPlan


class PaidPlanOnlyMiddleware:
    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
        access_level_required: int = 1,
    ):
        self.get_response = get_response
        self.access_level_required = access_level_required

    def __call__(self, request: HttpRequest) -> HttpResponse:
        user = request.user

        if user.is_authenticated:
            user_profile: Optional[UserProfile] = getattr(user, "user_profile", None)
            paid_plan: Optional[PaidPlan] = getattr(user_profile, "paid_plan", None)

            if paid_plan is None or paid_plan.access_level < self.access_level_required:
                return HttpResponseForbidden(
                    "Upgrade to a paid plan to access this resource."
                )

        return self.get_response(request)


def paid_plan_only_middleware(
    get_response: Callable[[HttpRequest], HttpResponse],
) -> PaidPlanOnlyMiddleware:
    return PaidPlanOnlyMiddleware(get_response, access_level_required=1)


def pro_plan_only_middleware(
    get_response: Callable[[HttpRequest], HttpResponse],
) -> PaidPlanOnlyMiddleware:
    return PaidPlanOnlyMiddleware(get_response, access_level_required=2)


def pro_plus_plan_only_middleware(
    get_response: Callable[[HttpRequest], HttpResponse],
) -> PaidPlanOnlyMiddleware:
    return PaidPlanOnlyMiddleware(get_response, access_level_required=3)


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
