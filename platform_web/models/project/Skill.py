import uuid
from typing import TYPE_CHECKING, cast

from django.db import models
from django.utils.translation import gettext_lazy as _

from platform_web.models.project.Course import Course
from platform_web.models.project.Project import Project


class Skill(models.Model):
    if TYPE_CHECKING:
        objects: models.Manager

    name = models.CharField(max_length=100)
    related_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="skills",
        verbose_name=_("Related course"),
    )
    projects = models.ManyToManyField(
        Project,
        blank=True,
        related_name="skills",
        help_text=cast(
            str, _("Projects shown under this skill on the roadmap")
        ),
    )
    order = models.PositiveIntegerField(
        default=0,  # type: ignore[arg-type]
        help_text=cast(str, _("Ordering for admin sorting")),
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
