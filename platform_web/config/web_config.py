from dataclasses import dataclass


def normalize_admin_url_path(admin_url: str) -> str:
    cleaned = str(admin_url or "").strip()
    if not cleaned:
        return ""
    return cleaned.rstrip("/") + "/"


@dataclass
class WebsiteConfigScheme:
    id: str = "id"
    site_name: str = "site_name"
    tagline: str = "tagline"


@dataclass
class WebsiteSettings:
    website_config: str = "website_config"
    admin_url: str = "cp/"
    admin_url_redirect: str = "/"
    social_media_links: str = "social_media_links"
    changelog: str = "changelog"