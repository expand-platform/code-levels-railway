import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Framework(models.Model):
    VUE = "Vue"
    REACT = "React"
    FASTAPI = "FastAPI"
    DJANGO = "Django"
    WORDPRESS = "WordPress"
    LARAVEL = "Laravel"
    EXPRESS = "Express"
    SPRING = "Spring"

    FRAMEWORK_CHOICES = [
        (VUE, "Vue"),
        (REACT, "React"),
        (DJANGO, "Django"),
        (WORDPRESS, "WordPress"),
        (LARAVEL, "Laravel"),
        (EXPRESS, "Express"),
        (SPRING, "Spring"),
        (FASTAPI, "FastAPI"),
    ]

    name = models.CharField(max_length=20, unique=True)
    order = models.PositiveIntegerField(
        default=5, help_text=_("Order for displaying frameworks")
    )
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)


    class Meta:
        db_table = "frameworks"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
