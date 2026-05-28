# from django.db import models
# from django.utils.translation import gettext_lazy as _

# ATTEMPT_STATUS_CHOICES = [
#     ("pending", _("Pending")),
#     ("in_progress", _("In Progress")),
#     ("success", _("Success")),
#     ("failed", _("Failed")),
# ]

# LANGUAGE_CHOICES = [
#     ("en", "English"),
#     ("ru", "Русский"),
# ]

# class TranslationJob(models.Model):
#     translation_uuid = models.UUIDField(db_index=True)
    
#     attempt_number = models.PositiveIntegerField(default=1)
    
#     source_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
#     target_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    
#     status = models.CharField(max_length=20, choices=ATTEMPT_STATUS_CHOICES, default="pending")
#     error_message = models.TextField(blank=True, null=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = "translation_logs"
#         ordering = ["-created_at"]