from django.db import models
from platform_web.models.app.project.Project import Project


class ProjectPart(models.Model):
    project = models.ForeignKey(Project, related_name="parts", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.project.title} - {self.title}"
