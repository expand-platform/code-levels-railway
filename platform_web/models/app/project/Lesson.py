import uuid

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from platform_web.models.app.project.Project import Project

from platform_web.data.transliteration import transliterate_ru_to_latin


TYPE_CHOICES = [
    ("theory", _("Theory")),
    ("video", _("Video")),
    ("exercise", _("Exercise")),
    ("task", _("Task")),
    ("mini-project", _("Mini-project")),
    ("project", _("Project")),
]



class Lesson(models.Model):
    project = models.ForeignKey(Project, related_name="parts", on_delete=models.CASCADE)
    
    title=models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True, blank=True)

    thumbnail = models.ImageField(upload_to="lesson_images/", blank=True, null=True)

    youtube_url = models.URLField(blank=True, null=True)
    codepen_url = models.URLField(blank=True, null=True)
    
    description=models.TextField(blank=True)
    objectives=models.TextField(
        blank=True, default="", help_text=_("List of lesson objectives")
    )

    order = models.PositiveIntegerField(default=0)
    
    seo_title=models.CharField(max_length=255, blank=True, default="")
    seo_description=models.TextField(blank=True, default="")

    slug=models.SlugField(max_length=255, blank=True)
    last_edited = models.DateTimeField(auto_now=True)
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    

    class Meta:
        db_table = "project_parts"
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            transliterated_title = transliterate_ru_to_latin(str(self.title))
            base_slug = slugify(transliterated_title)
            if not base_slug:
                base_slug = slugify(str(self.title))
            if not base_slug:
                base_slug = f"lesson-{str(self.uuid)[:8]}"

            slug = base_slug
            counter = 1
            while Lesson.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        title = self.title
        return str(title) if title else f"Lesson {self.pk}"
