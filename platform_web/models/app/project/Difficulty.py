import uuid

from django.db import models


class Difficulty(models.Model):
    LEVEL_EASY = "easy"
    LEVEL_MODERATE = "moderate"
    LEVEL_HARD = "hard"
    LEVEL_HARDCORE = "extreme"

    LEVEL_EASY_DESCRIPTIVE = "You can do this"
    LEVEL_MODERATE_DESCRIPTIVE = "Some effort required"
    LEVEL_HARD_DESCRIPTIVE = "Challenging"
    LEVEL_HARDCORE_DESCRIPTIVE = "For experts only"

    LEVEL_CHOICES = [
        (LEVEL_EASY, "Easy"),
        (LEVEL_MODERATE, "Moderate"),
        (LEVEL_HARD, "Hard"),
        (LEVEL_HARDCORE, "Hardcore"),
        (LEVEL_EASY_DESCRIPTIVE, "You can do this"),
        (LEVEL_MODERATE_DESCRIPTIVE, "Some effort required"),
        (LEVEL_HARD_DESCRIPTIVE, "Challenging"),
        (LEVEL_HARDCORE_DESCRIPTIVE, "For experts only"),
    ]
    name = models.CharField(max_length=20, unique=True)

    order = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        db_table = "difficulties"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
