from cProfile import label
from ctypes.macholib import framework
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.app.project.Difficulty import Difficulty
from platform_web.models.app.project.Stage import Stage
from platform_web.models.app.project.Skill import Skill
from platform_web.models.app.project.Framework import Framework
from platform_web.models.app.project.Course import Course

User = get_user_model()

class Project(models.Model):
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,  # Set to True for migration safety; set to False after data migration if needed
        blank=True  # Set to True for migration safety; set to False after data migration if needed
    )
    difficulty = models.ForeignKey(
        Difficulty, on_delete=models.SET_NULL, null=True, blank=True
    )
    programming_languages = models.ManyToManyField(
        ProgrammingLanguage, blank=True, help_text="Predefined programming languages"
    )
    framework = models.ManyToManyField(
        Framework, blank=True, help_text="Predefined frameworks", verbose_name="Frameworks"
    )
    skills = models.ManyToManyField(Skill, blank=True)
    stages = models.ManyToManyField(Stage, blank=True)
    image = models.ImageField(upload_to="project_images/", blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects"
        ordering = ["order", "title"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title




# users_involved = models.ManyToManyField(
#     User,
#     related_name="projects",
#     blank=True,
#     help_text="Users signed up for this project",
# )
# description = models.TextField(
#     blank=True, help_text="Description for the Dashboard"
# )
# icon = models.CharField(max_length=100, blank=True, help_text="CSS class for icon")
