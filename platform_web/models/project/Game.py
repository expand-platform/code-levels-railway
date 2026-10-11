from django.db import models

from platform_web.services.model.ImageUpload import ImageUploadService


def game_image_upload_to(instance, filename):
    return ImageUploadService.unique_path(filename, "game_images", "game")


class Game(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=game_image_upload_to, blank=True, null=True)

    description = models.TextField(blank=True)
    link = models.URLField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "games"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title
