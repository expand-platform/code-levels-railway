import uuid

from django.db import models
from django.utils.text import slugify


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    order = models.PositiveIntegerField(
        default=0, help_text="Order for displaying programming languages (lower comes first)"
    )
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    class Meta:
        db_table = "programming_languages"
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
