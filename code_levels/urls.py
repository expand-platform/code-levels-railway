from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from platform_web.sitemaps import sitemaps
from platform_web.views import robots_txt


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("api/", include("api.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    
    path("", include("platform_web.urls")),
    
    path("cp/", admin.site.urls),
    path("account/", include(("allauth.urls"))),
    
    path("summernote/", include("django_summernote.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]

# ? development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
