from django.db import models
from .website_config import WebsiteConfig


#? stored website data like site name, tagline, support email, etc.
class SocialMediaLink(models.Model):
    website_config = models.ForeignKey(WebsiteConfig, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="telegram")
    url = models.URLField(max_length=255, blank=True, null=True)
    

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Social Media Link"
        verbose_name_plural = "Social Media Links"
 
