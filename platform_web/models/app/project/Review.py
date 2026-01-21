from django.db import models
from django.contrib.auth import get_user_model

from platform_web.models.app.project.Submission import Submission
from platform_web.models.app.project.Skill import Skill

User = get_user_model()


class Review(models.Model):
    submission = models.OneToOneField(
        Submission, related_name="review", on_delete=models.CASCADE
    )
    reviewer = models.CharField(max_length=255)
    feedback = models.TextField()
    score = models.PositiveIntegerField(default=0)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.submission}"
