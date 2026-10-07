from functools import wraps
from typing import Callable, Optional

from django.http import HttpResponseForbidden, HttpRequest, HttpResponse
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
from django.utils.translation import gettext as _

from api.models.UserProfile import UserProfile
from code_levels.settings.features.feature_flags import COURSES, DASHBOARD
from platform_web.config.web_config import WebsiteSettings, normalize_admin_url_path
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


def feature_allowed(user, flag_name: str) -> bool:
    """Open to everyone when the flag is on. Staff only when it is off or missing."""
    flag = settings.FEATURE_FLAGS.get(flag_name)

    if flag is not None and flag.is_enabled():
        return True

    return bool(
        getattr(user, "is_authenticated", False) and getattr(user, "is_staff", False)
    )


def user_dashboard_allowed(user) -> bool:
    return feature_allowed(user, DASHBOARD)


def courses_allowed(user) -> bool:
    return feature_allowed(user, COURSES)


def require_feature(flag_name: str):
    """While the flag is off, only staff can open the view."""

    def decorator(view: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
        @wraps(view)
        def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            if feature_allowed(request.user, flag_name):
                return view(request, *args, **kwargs)

            if not request.user.is_authenticated:
                return redirect_to_login(reverse("projects"), settings.LOGIN_URL)

            return HttpResponseForbidden(_("Forbidden"))

        return wrapper

    return decorator


def require_user_dashboard(view: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    return require_feature(DASHBOARD)(view)


def require_courses(view: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    return require_feature(COURSES)(view)


class AdminStaffOnlyMiddleware:
    """
    Restrict admin route access to authenticated staff users only.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        path = request.path

        # Always allow static & media
        if path.startswith("/static/") or path.startswith("/media/"):
            return self.get_response(request)

        admin_route = normalize_admin_url_path(WebsiteSettings.admin_url)
        admin_path = f"/{admin_route.lstrip('/')}" if admin_route else ""

        is_admin_route = admin_path and path.startswith(admin_path)

        if is_admin_route:
            user = request.user

            if not user.is_authenticated:
                return redirect_to_login(path, settings.LOGIN_URL)

            if not user.is_staff:
                return HttpResponseForbidden("Forbidden")

        response = self.get_response(request)

        if is_admin_route:
            response["X-Robots-Tag"] = "noindex, nofollow, noarchive"

        return response
