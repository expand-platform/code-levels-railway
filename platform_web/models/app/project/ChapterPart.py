from django.db import models

class ChapterPart(models.Model):
    order = models.PositiveIntegerField(default=0)

    chapter = models.ForeignKey('platform_web.Chapter', on_delete=models.CASCADE, related_name='chapter_parts')
    part = models.ForeignKey('platform_web.Part', on_delete=models.CASCADE, related_name='chapter_links')

    class Meta:
        db_table = 'chapter_parts'
        ordering = ['order']
        unique_together = ('chapter', 'part')

    def __str__(self):
        return f"{self.chapter} - {self.part} (Order: {self.order})"

