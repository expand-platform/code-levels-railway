import uuid

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.app.project.Difficulty import Difficulty
from platform_web.models.app.project.Framework import Framework
from platform_web.models.app.project.Course import Course

from platform_web.data.transliteration import transliterate_ru_to_latin




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


class Project(models.Model):
    title=models.CharField(max_length=255)
    image = models.ImageField(upload_to="project_images/", blank=True, null=True)
    
    type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, default=TOPIC)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, blank=True, null=True, default="ru")
    
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
    
    description=models.TextField(blank=True, help_text=_("Description for the Dashboard"))
    stages=models.TextField(blank=True, null=True, default="")

    
    framework = models.ManyToManyField(
        Framework,
        blank=True,
        help_text=_("Predefined frameworks"),
        verbose_name=_("Frameworks"),
    )

    is_active = models.BooleanField(default=True)
    is_video_course = models.BooleanField(default=False)
    
    seo_title=models.CharField(max_length=255, blank=True, default="")
    seo_description=models.TextField(blank=True, default="")
   
    language_order = models.PositiveIntegerField(default=0)
    course_order = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(
        default=0, help_text=_("Ordering for admin sorting")
    )

    slug=models.SlugField(max_length=255, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects"
        ordering = ["order", "-updated_at"]

    def save(self, *args, **kwargs):
        title = self.title
        if not self.slug and title:
            transliterated_title = transliterate_ru_to_latin(str(title))
            base_slug = slugify(transliterated_title)
            if not base_slug:
                base_slug = slugify(str(title))
            if not base_slug:
                base_slug = f"project-{str(self.uuid)[:8]}"

            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        title = self.title
        return str(title) if title else f"Project {self.pk}"
