import uuid

from django.db import models
from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage

#! Make order sortable / drag-and-drop in admin

TYPE_CHOICES = [
    ("theory", "Theory"),
    ("video", "Video"),
    ("exercise", "Exercise"),
    ("task", "Task"),
    ("mini-project", "Mini-project"),
    ("project", "Project"),
]


class Lesson(models.Model):
    project = models.ForeignKey(Project, related_name="parts", on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True, blank=True)

    chapter = models.ForeignKey('platform_web.Chapter', related_name='parts', on_delete=models.CASCADE, null=True, blank=True)
    
    codepen_url = models.URLField(blank=True, null=True)
    objectives = models.JSONField(
        default=list,
        blank=True,
        help_text="List of lesson objectives"
    )
    languages = models.ManyToManyField(ProgrammingLanguage, blank=True)
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        db_table = "project_parts"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title
