import uuid

from django.db import models
from platform_web.models.project.ProgrammingLanguage import ProgrammingLanguage

from platform_web.services.model.SlugService import SlugService


class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    languages = models.ManyToManyField(
        ProgrammingLanguage, related_name="courses", blank=True
    )

    order = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        db_table = "courses"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = SlugService.generate_unique_slug(
                self.title,
                self.__class__,
                exclude_pk=self.pk,
                fallback_prefix="course",
            )
        super().save(*args, **kwargs)
