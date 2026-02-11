import uuid

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

TOPIC = "topic"
PROJECT = "project"

PROJECT_TYPE_CHOICES = [
    (TOPIC, "Topic"),
    (PROJECT, "Project"),
]

# ! Suggestions:
# 1. Ability to add your own programming languages and frameworks
# 2. Ability to select multiple courses (e.g., web app, mobile app, data science)
# 3. Difficulty levels unified (e.g., beginner, intermediate, advanced)
# 4. Add practice / mini-projects -> type

class Project(models.Model):
    title = models.CharField(max_length=255)
    
    language_order = models.PositiveIntegerField(default=0)
    course_order = models.PositiveIntegerField(default=0)
    
    image = models.ImageField(upload_to="project_images/", blank=True, null=True)
    # details_image = models.ImageField(upload_to="project_images/", blank=True, null=True)
    
    type = models.CharField(
        max_length=20,
        choices=PROJECT_TYPE_CHOICES,
        default=TOPIC,
    )

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="projects", null=True, blank=True
    )

    programming_languages = models.ManyToManyField(
        ProgrammingLanguage, blank=True, help_text="Predefined programming languages"
    )
    difficulty = models.ForeignKey(
        Difficulty, on_delete=models.SET_NULL, null=True, blank=True
    )
    framework = models.ManyToManyField(
        Framework,
        blank=True,
        help_text="Predefined frameworks",
        verbose_name="Frameworks",
    )
    skills = models.ManyToManyField(Skill, blank=True)
    stages = models.ManyToManyField(Stage, blank=True)

    description = models.TextField(
        blank=True, help_text="Description for the Dashboard"
    )
    stages = models.JSONField(default=list, blank=True, null=True)

    # Metadata
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    order = models.PositiveIntegerField(default=0, help_text="Ordering for admin sorting")

    class Meta:
        db_table = "projects"
        ordering = ["order", "-updated_at", "title"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
