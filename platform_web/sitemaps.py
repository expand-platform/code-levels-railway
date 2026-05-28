from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from typing import cast

from platform_web.models.project.Lesson import Lesson
from platform_web.models.project.Project import Project


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return ["home"]

    def location(self, obj):
        return reverse(cast(str, obj))


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
        project = cast(Project, obj)
        return reverse("project_details", kwargs={"slug": project.slug})


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
        lesson = cast(Lesson, obj)
        return reverse(
            "lesson_details",
            kwargs={"slug": lesson.project.slug, "order": lesson.order},
        )


sitemaps = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
    "lessons": LessonSitemap,
}