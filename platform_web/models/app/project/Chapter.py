from django.db import models
from platform_web.models.app.project.Part import Part
from platform_web.models.app.project.Project import Project

class Chapter(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="chapters"
    )
    parts = models.ManyToManyField(Part, related_name='chapter_set', blank=True)

    class Meta:
        db_table = "chapters"
        ordering = ["order", "title"]

    def __str__(self):
        return f"{self.project.title} - {self.title}"
