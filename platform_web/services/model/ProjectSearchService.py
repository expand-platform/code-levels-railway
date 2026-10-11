from django.urls import reverse

from platform_web.models.project.Project import Project, ProjectType


class ProjectSearchService:
    """Active project titles for the command-palette search."""

    @staticmethod
    def catalog() -> list[dict[str, str]]:
        projects = (
            Project.objects.filter(is_active=True, type=ProjectType.PROJECT)
            .exclude(slug="")
            .select_related("course")
            .only("title", "slug", "course__title")
            .order_by("title")
        )
        items = []
        for project in projects:
            course = project.course
            items.append(
                {
                    "title": project.title,
                    "url": reverse("project_details", kwargs={"slug": project.slug}),
                    "course": course.title if course is not None else "",
                }
            )
        return items
