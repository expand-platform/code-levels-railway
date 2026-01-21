from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.app.project.Difficulty import Difficulty
from platform_web.models.app.project.DevelopmentStage import DevelopmentStage
from platform_web.models.app.project.Skill import Skill

User = get_user_model()


class Project(models.Model):
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="project_images/", blank=True, null=True)
    programming_languages = models.ManyToManyField(
        ProgrammingLanguage, blank=True, help_text="Predefined programming languages"
    )
    difficulty = models.ForeignKey(
        Difficulty, on_delete=models.SET_NULL, null=True, blank=True
    )
    skills = models.ManyToManyField(Skill, blank=True)
    stages = models.ManyToManyField(DevelopmentStage, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # users = models.ManyToManyField(
    #     User,
    #     related_name="projects",
    #     blank=True,
    #     help_text="Users signed up for this project",
    # )
    # description = models.TextField(
    #     blank=True, help_text="Description for the Dashboard"
    # )
    # icon = models.CharField(max_length=100, blank=True, help_text="CSS class for icon")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
