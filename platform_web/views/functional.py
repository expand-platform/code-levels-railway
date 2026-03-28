from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils.translation import activate, get_supported_language_variant
from django.utils.http import url_has_allowed_host_and_scheme



class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class NotFoundView(TemplateView):
    template_name = "website/pages/404.html"


class NotFoundPreview(TemplateView):
    template_name = "website/pages/404.html"


# not found 404
def not_found_404(request, exception):
    not_found_404_view = NotFoundView.as_view()
    return not_found_404_view(request, exception=exception)


@require_POST
def set_language_and_save(request):
    """Set language from header selector, save to user profile if authenticated,
    set session + cookie and redirect to `next`.
    """
    lang_code = request.POST.get("language")
    next_url = request.POST.get("next") or "/"

    # normalize/validate language code
    try:
        lang_code = get_supported_language_variant(lang_code)
    except Exception:
        lang_code = settings.LANGUAGE_CODE

    # persist to profile if authenticated
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        try:
            from api.models import UserProfile

            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.interface_language = lang_code
            profile.save(update_fields=["interface_language"])
        except Exception:
            # keep best-effort: don't fail on DB errors
            pass

    # set in session and activate for this request
    try:
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
    except Exception:
        pass
    activate(lang_code)

    # validate next URL
    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next_url = "/"

    response = redirect(next_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response
