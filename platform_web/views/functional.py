from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout
from django.shortcuts import redirect


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
