import uuid

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from platform_web.models.app.project.Project import Project


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
    objectives=models.JSONField(
        default=list, blank=True, help_text=_("List of lesson objectives")
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
        if self._state.adding and not self.slug and self.title:
            self.slug = slugify(str(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        title = self.title
        return str(title) if title else f"Lesson {self.pk}"
