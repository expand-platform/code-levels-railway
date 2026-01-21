from django.db import models


class Difficulty(models.Model):
    LEVEL_EASY = "easy"
    LEVEL_MODERATE = "moderate"
    LEVEL_HARD = "hard"
    LEVEL_CHOICES = [
        (LEVEL_EASY, "Easy"),
        (LEVEL_MODERATE, "Moderate"),
        (LEVEL_HARD, "Hard"),
    ]
    name = models.CharField(max_length=20, choices=LEVEL_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()
