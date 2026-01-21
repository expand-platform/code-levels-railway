from django.db import models
from django.core.exceptions import ValidationError


# ? stored website data like site name, tagline, support email, etc.
class WebsiteConfig(models.Model):
    site_name = models.CharField(max_length=255, default="Zay")
    tagline = models.CharField(max_length=255, default="Gadgets that love you")

    def __str__(self):
        return "Website Configuration"

    class Meta:
        verbose_name = "Website Configuration"
        verbose_name_plural = "Website Configuration"

    # ? only one instance editing allowed
    def save(self, *args, **kwargs):
        if not self.pk and WebsiteConfig.objects.exists():
            raise ValidationError("There can be only one WebConfig instance")
        return super().save(*args, **kwargs)
