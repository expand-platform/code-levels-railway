from platform_web.models.base.website_config import WebsiteConfig


class SeoService:
    @staticmethod
    def generate_initial_seo_title(project_title):
        config = WebsiteConfig.objects.first()
        site_name = config.site_name if config else "CodeLevels"
        return f"{project_title} | {site_name}"
    
    @staticmethod
    def generate_initial_seo_description(project_title):
        config = WebsiteConfig.objects.first()
        site_name = config.site_name if config else "CodeLevels"
        return f"{project_title} | {site_name}"