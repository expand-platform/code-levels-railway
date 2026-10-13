from django.urls import reverse
from django.utils.translation import gettext as _

from platform_web.models.project.Course import Course, CourseType
from platform_web.models.project.Game import Game
from platform_web.models.project.Project import Project, ProjectType


class SearchService:
    """Active projects, games, and roadmaps for the command-palette search."""

    @staticmethod
    def catalog() -> list[dict[str, str]]:
        return [
            *SearchService._projects(),
            *SearchService._games(),
            *SearchService._roadmaps(),
        ]

    @staticmethod
    def _item(title, url, group, kind) -> dict[str, str]:
        return {"title": title, "url": url, "course": group, "kind": kind}

    @staticmethod
    def _projects() -> list[dict[str, str]]:
        projects = (
            Project.objects.filter(is_active=True, type=ProjectType.PROJECT)
            .exclude(slug="")
            .select_related("course")
            .only("title", "slug", "course__title")
            .order_by("title")
        )
        return [
            SearchService._item(
                project.title,
                reverse("project_details", kwargs={"slug": project.slug}),
                project.course.title if project.course is not None else "",
                "project",
            )
            for project in projects
        ]

    @staticmethod
    def _games() -> list[dict[str, str]]:
        games = Game.objects.exclude(link="").only("title", "link").order_by("title")
        label = _("Game")
        return [
            SearchService._item(game.title, game.link, label, "game")
            for game in games
        ]

    @staticmethod
    def _roadmaps() -> list[dict[str, str]]:
        courses = (
            Course.objects.filter(type=CourseType.LANGUAGE)
            .exclude(slug="")
            .only("title", "slug")
            .order_by("title")
        )
        label = _("Roadmap")
        return [
            SearchService._item(
                course.title,
                reverse("roadmaps_by_course", kwargs={"course_slug": course.slug}),
                label,
                "roadmap",
            )
            for course in courses
        ]
