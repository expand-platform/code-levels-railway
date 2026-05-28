from django.db import models
from django.utils.translation import gettext_lazy as _

from platform_web.models.jobs.BackgroundJob import BackgroundJob

ATTEMPT_STATUS_CHOICES = [
    ("pending", _("Pending")),
    ("in_progress", _("In Progress")),
    ("success", _("Success")),
    ("failed", _("Failed")),
]

ENTITY_TYPE_CHOICES = [
    ("project", _("Project")),
    ("lesson", _("Lesson")),
]

LANGUAGE_CHOICES = [
    ("en", "English"),
    ("ru", "Русский"),
]

class TranslationLog(models.Model):
    background_job = models.ForeignKey(
        BackgroundJob,
        on_delete=models.SET_NULL,
        related_name="translation_logs",
        blank=True,
        null=True,
    )
    translation_uuid = models.UUIDField()

    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    source_object_id = models.PositiveIntegerField()
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    
    attempt_number = models.PositiveIntegerField(default=1)
    
    source_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    target_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    
    status = models.CharField(max_length=20, choices=ATTEMPT_STATUS_CHOICES, default="pending")
    
    error_code = models.CharField(max_length=100, blank=True, default="")
    error_message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "translation_logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["background_job", "created_at"], name="trlog_job_created_idx"),
            models.Index(fields=["status", "created_at"], name="trlog_status_created_idx"),
            models.Index(
                fields=["translation_uuid", "source_language", "target_language", "created_at"],
                name="trlog_group_lang_created_idx",
            ),
            models.Index(fields=["entity_type", "source_object_id"], name="trlog_entity_source_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(source_language=models.F("target_language")),
                name="translationlog_source_target_different",
            ),
            models.CheckConstraint(
                condition=models.Q(attempt_number__gte=1),
                name="translationlog_attempt_positive",
            ),
            models.UniqueConstraint(
                fields=[
                    "translation_uuid",
                    "source_language",
                    "target_language",
                    "attempt_number",
                ],
                name="translationlog_unique_attempt_per_direction",
            ),
        ]