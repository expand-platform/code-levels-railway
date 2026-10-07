import uuid
from typing import cast

from django.db import models
from django.utils.translation import gettext_lazy as _

from platform_web.models.project.Course import Course
from platform_web.models.project.Project import Project


class Skill(models.Model):
    name = models.CharField(max_length=100)
    related_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="skills",
        verbose_name=_("Course"),
    )
    projects = models.ManyToManyField(
        Project,
        blank=True,
        related_name="skills",
        help_text=_("Projects shown under this skill on the roadmap"),
    )
    contents = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Content"),
        help_text=cast(
            str,
            _(
                "Numbered list shown under this skill on the course timeline when it has no projects."
            ),
        ),
    )
    order = models.PositiveIntegerField(
        default=0,  # type: ignore[arg-type]
        help_text=_("Ordering for admin sorting"),
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        db_table = "skills"
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["related_course", "name"],
                name="skill_name_unique_per_course",
            ),
        ]

    def __str__(self):
        return self.name
