from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse



urlpatterns = [
    path("api/", include("api.urls")),
    
    path("", include("platform_web.urls")),
    
    path("cp/", admin.site.urls),
    path("account/", include(("allauth.urls"))),
    
    # path("health/", lambda r: HttpResponse("OK"), name="health"),
    path("summernote/", include("django_summernote.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]

# ? development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
