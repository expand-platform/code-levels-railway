import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from platform_web.mixins.SeoSlugMixin import SeoSlugMixin
from platform_web.models.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.project.Difficulty import Difficulty
from platform_web.models.project.Framework import Framework
from platform_web.models.project.Course import Course


TOPIC = "topic"
PROJECT = "project"
GUIDE = "guide"

PROJECT_TYPE_CHOICES = [
    (TOPIC, _("Topic")),
    (PROJECT, _("Project")),
    (GUIDE, _("Guide")),
]

LANGUAGE_CHOICES = [
    ("en", "English"),
    ("ru", "Русский"),
]

TRANSLATION_STATUS_CHOICES = [
    ("not_translated", _("Not translated")),
    ("translated", _("Translated")),
    ("failed", _("Failed")),
]


class Project(SeoSlugMixin, models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="project_images/", blank=True, null=True)

    type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, default=TOPIC)
    # language = models.CharField(
    #     max_length=50, choices=LANGUAGE_CHOICES, blank=True, null=True, default="ru"
    # )

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="projects", null=True, blank=True
    )
    programming_languages = models.ManyToManyField(
        ProgrammingLanguage, blank=True, help_text=_("Predefined programming languages")
    )

    difficulty = models.ForeignKey(
        Difficulty, on_delete=models.SET_NULL, null=True, blank=True
    )
    codepen_url = models.URLField(blank=True, null=True)

    description = models.TextField(
        blank=True, help_text=_("Description for the Dashboard")
    )
    stages = models.TextField(blank=True, null=True, default="")

    framework = models.ManyToManyField(
        Framework,
        blank=True,
        help_text=_("Predefined frameworks"),
        verbose_name=_("Frameworks"),
    )

    is_active = models.BooleanField(default=True)
    is_video_course = models.BooleanField(default=False)

    language_order = models.PositiveIntegerField(default=0)
    course_order = models.PositiveIntegerField(default=0)

    slug = models.SlugField(max_length=255, blank=True)
    
    seo_title = models.CharField(max_length=255, blank=True, default="")
    seo_description = models.TextField(blank=True, default="")
    
    order = models.PositiveIntegerField(
        default=0, help_text=_("Ordering for admin sorting")
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    translation_uuid = models.UUIDField(blank=True, null=True, db_index=True)
    translation_status = models.CharField(max_length=50, choices=TRANSLATION_STATUS_CHOICES, blank=True, null=True)
    translated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "projects"
        ordering = ["order", "-updated_at"]

    def __str__(self):
        title = self.title
        return str(title) if title else f"Project {self.pk}"