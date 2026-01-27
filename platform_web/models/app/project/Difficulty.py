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
    name = models.CharField(max_length=20, choices=LEVEL_CHOICES, unique=True)

    class Meta:
        db_table = "difficulties"
        ordering = ["name"]

    def __str__(self):
        return self.get_name_display()
