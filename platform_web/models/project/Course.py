import os
import uuid
from dataclasses import dataclass

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from platform_web.models.project.ProgrammingLanguage import ProgrammingLanguage

from platform_web.services.model.SlugService import SlugService


@dataclass
class CourseType:
    REGULAR: str = "regular"
    LANGUAGE: str = "language"
    JOB: str = "job"
    GUIDE: str = "guide"


COURSE_TYPE_CHOICES = [
    (CourseType.REGULAR, _("Regular course")),
    (CourseType.LANGUAGE, _("Language course")),
    (CourseType.JOB, _("Job course")),
    (CourseType.GUIDE, _("Guide")),
]


def course_image_upload_to(instance, filename):
    base, ext = os.path.splitext(os.path.basename(filename))
    stem = slugify(base)[:60] or "course"
    tail = uuid.uuid4().hex[:8]
    return f"course_images/{stem}-{tail}{ext.lower()}"


class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to=course_image_upload_to,
        blank=True,
        null=True,
        verbose_name=_("Image"),
    )
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    languages = models.ManyToManyField(
        ProgrammingLanguage, related_name="courses", blank=True
    )
    type = models.CharField(
        max_length=20,
        choices=COURSE_TYPE_CHOICES,
        default=CourseType.REGULAR,
        verbose_name=_("Course type"),
    )

    order = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        db_table = "courses"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = SlugService.generate_unique_slug(
                self.title,
                models.Model, self.__class__,
                exclude_pk=self.pk,
                fallback_prefix="course",
            )
        super().save(*args, **kwargs)
