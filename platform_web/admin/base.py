from django.contrib import admin
from django.http import HttpRequest

from platform_web.config.web_config import WebsiteConfigScheme

from platform_web.models.base import WebsiteConfig
from platform_web.models.base import SocialMediaLink

# inlines
class InlineSocialMediaLink(admin.TabularInline):
    model = SocialMediaLink
    extra = 1

class WebsiteConfigAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WebsiteConfig._meta.fields]
    list_display_links = (WebsiteConfigScheme.id, WebsiteConfigScheme.site_name) 
    inlines = [InlineSocialMediaLink]

    # Only allow add if no config exists
    def has_add_permission(self, request: HttpRequest):
        return not WebsiteConfig.objects.exists()

admin.site.register(WebsiteConfig, WebsiteConfigAdmin)
admin.site.register(SocialMediaLink)