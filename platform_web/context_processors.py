from platform_web.middleware import courses_allowed, user_dashboard_allowed
from platform_web.models.base.social_media_link import SocialMediaLink
from platform_web.models.base.website_config import WebsiteConfig
from platform_web.models.base import Changelog
from django.http import HttpRequest
from platform_web.config.web_config import WebsiteSettings
from django.utils.translation import gettext_lazy as _
from platform_web.models.project.Course import Course, CourseType
from platform_web.models.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.project.Project import ProjectType

website_title = _("CodeLevels")
website_tagline = _("Your step-by-step coding journey")

#! TODO: refactor context processors to use only queries that page needs


def _sidebar_courses(course_type):
    # Courses with no skills are empty. A skill with no projects still counts.
    return (
        Course.objects.filter(type=course_type, skills__isnull=False)
        .distinct()
        .order_by("order", "title")
    )


def _get_sidebar_project_courses():
    return _sidebar_courses(CourseType.REGULAR)


def _get_sidebar_job_courses():
    return _sidebar_courses(CourseType.JOB)


def _get_sidebar_language_courses():
    return _sidebar_courses(CourseType.LANGUAGE)


def _get_sidebar_topic_languages():
    return (
        ProgrammingLanguage.objects.filter(project__is_active=True, project__type=ProjectType.TOPIC)
        .distinct()
        .order_by("order", "name")
    )


def website_config(request: HttpRequest) -> dict:
    website_config = WebsiteConfig.objects.order_by('id').first()
    if website_config is None:
        website_config = WebsiteConfig(site_name=website_title, tagline=website_tagline)
    # Переводим tagline перед передачей в шаблон
    website_config.tagline = _(website_config.tagline)
    social_media_links = list(SocialMediaLink.objects.all())
    discord_url = ""
    telegram_url = ""
   
    for link in social_media_links:
        name = (link.name or "").lower()
        if not link.url:
            continue
        if "discord" in name and not discord_url:
            discord_url = link.url
        elif "telegram" in name and not telegram_url:
            telegram_url = link.url
    
    changelog = Changelog.objects.order_by('-released_at').first()
    user_dashboard_enabled = user_dashboard_allowed(request.user)
    courses_enabled = courses_allowed(request.user)
    sidebar_job_courses = _get_sidebar_job_courses()
    sidebar_project_courses = _get_sidebar_project_courses()
    sidebar_language_courses = _get_sidebar_language_courses()
    sidebar_topic_languages = _get_sidebar_topic_languages()

    return {
        WebsiteSettings.website_config: website_config,
        WebsiteSettings.social_media_links: social_media_links,
        WebsiteSettings.changelog: changelog,
        'sidebar_job_courses': sidebar_job_courses,
        'sidebar_project_courses': sidebar_project_courses,
        'sidebar_language_courses': sidebar_language_courses,
        'sidebar_topic_languages': sidebar_topic_languages,
        'discord_url': discord_url,
        'telegram_url': telegram_url,
        'user_dashboard_enabled': user_dashboard_enabled,
        'courses_enabled': courses_enabled,
    }
