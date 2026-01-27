from django.db import models
from platform_web.models.app.project.Chapter import Chapter
from platform_web.models.app.project.Part import Part

class ChapterPart(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="chapter_parts")
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name="chapter_links")
    order = models.PositiveIntegerField(default=0)
    custom_title = models.CharField(max_length=255, blank=True, help_text="Override the part title for this chapter context.")

    class Meta:
        db_table = "chapter_parts"
        ordering = ["order"]
        unique_together = ("chapter", "part")

    def __str__(self):
        title = self.custom_title if self.custom_title else str(self.part)
        return f"{self.chapter} - {title} (order: {self.order})"
