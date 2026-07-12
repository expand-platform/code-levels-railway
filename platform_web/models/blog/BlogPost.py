import uuid
from django.db import models
from django.utils import timezone

from platform_web.mixins.SeoSlugMixin import SeoSlugMixin
from platform_web.services.model.ExcerptService import ExcerptService


class BlogPost(SeoSlugMixin, models.Model):
    """Blog post model with SEO, publishing, and featured content support."""
    
    # Basic fields
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(blank=True)
    
    excerpt = models.CharField(
        max_length=500,
        blank=True,
        help_text="Brief summary for preview/SEO. Auto-generated if left empty."
    )
    
    # Media
    featured_image = models.ImageField(
        upload_to="blog/images/",
        blank=True,
        null=True
    )
    
    # Metadata
    slug = models.SlugField(max_length=255, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    # Publishing
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    
    # Organization
    order = models.PositiveIntegerField(default=0)
    
    # SEO
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "blog_posts"
        ordering = ["-published_at", "order"]
        verbose_name_plural = "Blog Posts"
    
    def save(self, *args, **kwargs):
        if not self.excerpt and self.content:
            self.excerpt = self._generate_excerpt()

        if self.is_published and not self.published_at:
            self.published_at = timezone.now()

        if self.is_published and not self.seo_title:
            self.seo_title = self.title[:70]

        if self.is_published and not self.seo_description:
            self.seo_description = (self.excerpt or self.title)[:160]

        super().save(*args, **kwargs)
    
    def _generate_excerpt(self, max_length: int = 200, word_count: int = 30) -> str:
        """Generate excerpt from content using the shared excerpt service."""
        return ExcerptService.generate_excerpt(self.content, max_length=max_length, word_count=word_count)
    
    def __str__(self):
        return self.title or f"BlogPost {self.pk}"