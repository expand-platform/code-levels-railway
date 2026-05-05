import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from platform_web.mixins.SeoSlugMixin import SeoSlugMixin
from platform_web.models.app.project.Project import Project


TYPE_CHOICES = [
    ("theory", _("Theory")),
    ("video", _("Video")),
    ("exercise", _("Exercise")),
    ("task", _("Task")),
    ("mini-project", _("Mini-project")),
    ("project", _("Project")),
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

    order = models.PositiveIntegerField(default=0)
    
    seo_title=models.CharField(max_length=255, blank=True, default="")
    seo_description=models.TextField(blank=True, default="")

    slug=models.SlugField(max_length=255, blank=True)
    last_edited = models.DateTimeField(auto_now=True)
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    

    class Meta:
        db_table = "project_parts"
        ordering = ["order"]
        
    def __str__(self):
        title = self.title
        return str(title) if title else f"Lesson {self.pk}"

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.fill_seo_on_creation()
        
    #     if not self.slug and self.title:
    #         self.slug = SlugService.generate_unique_slug(
    #             self.title, Lesson, exclude_pk=self.pk, fallback_prefix="lesson"
    #         )
    #     super().save(*args, **kwargs)
        
    # def fill_seo_on_creation(self):
    #     if not self.seo_title:
    #         self.seo_title = SeoService.generate_initial_seo_title(self.title)
    #     if not self.seo_description:
    #         self.seo_description = SeoService.generate_initial_seo_description(self.title)

 
