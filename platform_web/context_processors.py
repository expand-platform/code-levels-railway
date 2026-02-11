from platform_web.models.base.social_media_link import SocialMediaLink
from platform_web.models.base.website_config import WebsiteConfig
from django.http import HttpRequest
from platform_web.config.web_config import WebsiteSettings

website_title = "CodeLevels"
website_tagline = "Your step-by-step coding journey"

def website_config(request: HttpRequest) -> dict:
    website_config = WebsiteConfig.objects.order_by('id').first()
    
    if website_config is None:
        website_config = WebsiteConfig(site_name=website_title, tagline=website_tagline)
    social_media_links = SocialMediaLink.objects.all()
    
    return {
        WebsiteSettings.website_config: website_config,
        WebsiteSettings.social_media_links: social_media_links,
    }
