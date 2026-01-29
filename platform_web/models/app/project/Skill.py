import uuid

from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0, help_text="Order for displaying skills (lower comes first)")

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        db_table = "skills"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

