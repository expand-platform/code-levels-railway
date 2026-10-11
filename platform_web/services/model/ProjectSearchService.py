from django.urls import reverse
from django.utils.translation import gettext as _

from platform_web.models.project.Game import Game
from platform_web.models.project.Project import Project, ProjectType


#! TODO: could this code and queries be optimized?
class ProjectSearchService:
    """Active project and game titles for the command-palette search."""

    @staticmethod
    def catalog() -> list[dict[str, str]]:
        projects = (
            Project.objects.filter(is_active=True, type=ProjectType.PROJECT)
            .exclude(slug="")
            .select_related("course")
            .only("title", "slug", "course__title")
            .order_by("title")
        )
        games = Game.objects.exclude(link="").only("title", "link").order_by("title")
        game_label = _("Game")
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

        for game in games:
            items.append(
                {
                    "title": game.title,
                    "url": game.link,
                    "course": game_label,
                }
            )
        return items
