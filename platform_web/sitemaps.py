from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from platform_web.models.app.project.Lesson import Lesson
from platform_web.models.app.project.Project import Project


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return (
            Project.objects.filter(is_active=True, slug__isnull=False)
            .exclude(slug="")
            .order_by("order", "-updated_at")
        )

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        lang = obj.language if obj.language in {"en", "ru"} else "en"
        return reverse("project_details", kwargs={"lang": lang, "slug": obj.slug})


class LessonSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return (
            Lesson.objects.select_related("project")
            .filter(project__is_active=True, project__slug__isnull=False)
            .exclude(project__slug="")
            .order_by("project__order", "order")
        )

    def lastmod(self, obj):
        return obj.last_edited

    def location(self, obj):
        project_lang = obj.project.language if obj.project.language in {"en", "ru"} else "en"
        return reverse(
            "lesson_details",
            kwargs={"lang": project_lang, "slug": obj.project.slug, "order": obj.order},
        )


sitemaps = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
    "lessons": LessonSitemap,
}