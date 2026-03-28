from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("api/", include("api.urls")),
    
    path("", include("platform_web.urls")),
    
    path("cp/", admin.site.urls),
    path("account/", include(("allauth.urls"))),
    
    path("summernote/", include("django_summernote.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]

# ? development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
