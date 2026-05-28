import uuid

from django.db import models


class Difficulty(models.Model):
    name = models.CharField(max_length=20, unique=True)

    order = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        db_table = "difficulties"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
