from django.contrib import admin
from django.http import HttpRequest

from platform_web.config.web_config import WebsiteConfigScheme
from platform_web.models.base import SocialMediaLink
from platform_web.models.base import WebsiteConfig


class InlineSocialMediaLink(admin.TabularInline):
    model = SocialMediaLink
    extra = 1


@admin.register(WebsiteConfig)
class WebsiteConfigAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WebsiteConfig._meta.fields]
    list_display_links = (WebsiteConfigScheme.id, WebsiteConfigScheme.site_name)
    inlines = [InlineSocialMediaLink]

    def has_add_permission(self, request: HttpRequest):
        return not WebsiteConfig.objects.exists()


admin.site.register(SocialMediaLink)
