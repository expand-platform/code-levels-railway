from django.db import models
from django.contrib.auth import get_user_model

from platform_web.models.app.project.Skill import Skill

User = get_user_model()


class Certificate(models.Model):
    user = models.ForeignKey(
        User, related_name="certificates", on_delete=models.CASCADE
    )
    skills = models.ManyToManyField(Skill)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.user.username}"
