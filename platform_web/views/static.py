from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse


class HomeView(TemplateView):
    template_name = "website/pages/home.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/dashboard.html"


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(
        reverse("django.contrib.sitemaps.views.sitemap")
    )
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /cp/",
            "Disallow: /account/",
            "Disallow: /dashboard/",
            f"Sitemap: {sitemap_url}",
        ]
    )
    return HttpResponse(f"{content}\n", content_type="text/plain")
