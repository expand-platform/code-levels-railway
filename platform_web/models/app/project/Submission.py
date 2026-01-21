from django.db import models
from django.contrib.auth import get_user_model

from platform_web.models.app.project.ProjectPart import ProjectPart
from platform_web.models.app.project.Skill import Skill

User = get_user_model()

class Submission(models.Model):
    user = models.ForeignKey(User, related_name="submissions", on_delete=models.CASCADE)
    part = models.ForeignKey(ProjectPart, related_name="submissions", on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"Submission by {self.user.username} for {self.part.title}"