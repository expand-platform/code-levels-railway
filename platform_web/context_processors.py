from platform_web.models.base.social_media_link import SocialMediaLink
from platform_web.models.base.website_config import WebsiteConfig
from platform_web.models.base import Changelog
from django.http import HttpRequest
from platform_web.config.web_config import WebsiteSettings
from django.utils.translation import gettext_lazy as _
from platform_web.models.project.Course import Course
from platform_web.models.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.project.Project import PROJECT, TOPIC

website_title = _("CodeLevels")
website_tagline = _("Your step-by-step coding journey")


def _get_sidebar_project_courses():
    return (
        Course.objects.filter(projects__is_active=True, projects__type=PROJECT)
        .distinct()
        .order_by("order", "title")
    )


def _get_sidebar_topic_languages():
    return (
        ProgrammingLanguage.objects.filter(project__is_active=True, project__type=TOPIC)
        .distinct()
        .order_by("order", "name")
    )

def website_config(request: HttpRequest) -> dict:
    website_config = WebsiteConfig.objects.order_by('id').first()
    if website_config is None:
        website_config = WebsiteConfig(site_name=website_title, tagline=website_tagline)
    # Переводим tagline перед передачей в шаблон
    website_config.tagline = _(website_config.tagline)
    social_media_links = SocialMediaLink.objects.all()
    changelog = Changelog.objects.order_by('-released_at').first()
    sidebar_project_courses = _get_sidebar_project_courses()
    sidebar_topic_languages = _get_sidebar_topic_languages()

    return {
        WebsiteSettings.website_config: website_config,
        WebsiteSettings.social_media_links: social_media_links,
        WebsiteSettings.changelog: changelog,
        'sidebar_project_courses': sidebar_project_courses,
        'sidebar_topic_languages': sidebar_topic_languages,
    }
