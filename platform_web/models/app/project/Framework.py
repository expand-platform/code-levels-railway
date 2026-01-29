import uuid

from django.db import models


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

    name = models.CharField(max_length=20, choices=FRAMEWORK_CHOICES, unique=True)
    order = models.PositiveIntegerField(
        default=0, help_text="Order for displaying frameworks (lower comes first)"
    )
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)


    class Meta:
        db_table = "frameworks"
        ordering = ["order", "name"]

    def __str__(self):
        return self.get_name_display()
