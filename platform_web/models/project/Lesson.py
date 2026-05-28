import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from platform_web.mixins.SeoSlugMixin import SeoSlugMixin
from platform_web.models.project.Project import Project


TYPE_CHOICES = [
    ("theory", _("Theory")),
    ("video", _("Video")),
    ("exercise", _("Exercise")),
    ("task", _("Task")),
    ("mini-project", _("Mini-project")),
    ("project", _("Project")),
]

TRANSLATION_STATUS_CHOICES = [
    ("not_translated", _("Not translated")),
    ("translated", _("Translated")),
    ("failed", _("Failed")),
]



class Lesson(SeoSlugMixin, models.Model):
    project = models.ForeignKey(Project, related_name="parts", on_delete=models.CASCADE)
    
    title=models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="theory", blank=True)

    thumbnail = models.ImageField(upload_to="lesson_images/", blank=True, null=True)

    youtube_url = models.URLField(blank=True, null=True)
    codepen_url = models.URLField(blank=True, null=True)
    
    description=models.TextField(blank=True)
    objectives=models.TextField(
        blank=True, default="", help_text=_("List of lesson objectives")
    )

    
    slug=models.SlugField(max_length=255, blank=True)
    
    seo_title=models.CharField(max_length=255, blank=True, default="")
    seo_description=models.TextField(blank=True, default="")

    
    order = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    translation_uuid = models.UUIDField(blank=True, null=True, db_index=True)
    translation_status = models.CharField(max_length=50, choices=TRANSLATION_STATUS_CHOICES, blank=True, null=True)
    translated_at = models.DateTimeField(blank=True, null=True)
    
    last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "project_parts"
        ordering = ["order"]
        
    def __str__(self):
        title = self.title
        return str(title) if title else f"Lesson {self.pk}"

  

 
