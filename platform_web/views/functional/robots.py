from django.http import HttpResponse, HttpRequest
from django.urls import reverse


def robots_txt(request: HttpRequest) -> HttpResponse:
    sitemap_url = request.build_absolute_uri(
        reverse("django.contrib.sitemaps.views.sitemap")
    )
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /account/",
            "Disallow: /settings/",
            f"Sitemap: {sitemap_url}",
        ]
    )
    return HttpResponse(f"{content}\n", content_type="text/plain")
