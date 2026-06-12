from functools import wraps
from typing import Callable, Optional

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

from api.models.UserProfile import UserProfile
from platform_web.models.user.PaidPlan import PaidPlan


def paid_plan_required(access_level_required: int):
    def decorator(view_func: Callable):
        @wraps(view_func)
        def _wrapped_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            user = request.user

            if not user.is_authenticated:
                return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)

            user_profile: Optional[UserProfile] = getattr(user, "user_profile", None)
            paid_plan: Optional[PaidPlan] = getattr(user_profile, "paid_plan", None)

            if paid_plan is None or paid_plan.access_level < access_level_required:
                return HttpResponseForbidden(
                    "Upgrade to a paid plan to access this resource."
                )

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator

paid_plans_only = paid_plan_required(1)
pro_plan_required = paid_plan_required(2)
pro_plus_plan_required = paid_plan_required(3)