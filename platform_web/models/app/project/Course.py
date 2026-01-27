from django.db import models
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    languages = models.ManyToManyField(
        ProgrammingLanguage,
        related_name="courses",
        blank=True
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "courses"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title
