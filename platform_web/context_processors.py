from platform_web.models.base.social_media_link import SocialMediaLink
from platform_web.models.base.website_config import WebsiteConfig
from django.http import HttpRequest, HttpResponse
from platform_web.config.web_config import WebsiteSettings


def website_config(request: HttpRequest) -> dict:
    website_config = WebsiteConfig.objects.first()
    social_media_links = SocialMediaLink.objects.all()
    
    return {
        WebsiteSettings.website_config: website_config,
        WebsiteSettings.social_media_links: social_media_links,
    }
